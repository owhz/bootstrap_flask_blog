import time
import uuid

from pickle import dumps as pickle_dumps
from pickle import loads as pickle_loads

import redis


class FlaskRedisException(Exception):
    pass


class _Hash:

    __slots__ = 'hash_value'

    def __init__(self, key):
        self.hash_value = hash(key)

    def __hash__(self):
        return self.hash_value


def _make_key(args, kwargs):
    """
    create hash key from args and kwargs
    :param args:
    :param kwargs:
    :return:
    """
    key = args
    key += kwargs.keys() + kwargs.values()

    return _Hash(key)


class Redis:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        if 'REDIS_URI' not in app.config:
            raise FlaskRedisException('No REDIS_URI found in app config.')
        self.app = app
        self.conn = redis.Redis.from_url(self.app.config['REDIS_URI'])

    def __getattr__(self, item):
        # proxy self.redis
        return getattr(self.conn, item)

    def hash_cache(self, key, field_finder=lambda x: x.id, expiration=3600 * 24):
        """
        cache hash data
        :param key: hash key
        :param field_finder: hash field
        :param expiration: expiration time in second
        :return:
        """

        def wrapper(func):
            def inner(*args, **kwargs):
                data = self.hgetall(key)
                if data:
                    return [pickle_loads(item) for item in data.values()]
                data = func(*args, **kwargs)
                if data:
                    self.hmset(key, {field_finder(item): pickle_dumps(item) for item in data})
                return data

            return inner

        return wrapper

    def list_cache(self, expiration=3600 * 24):
        """
        cache list data
        :param expiration: expiration time in second
        :return:
        """

        def wrapper(func):
            def inner(*args, **kwargs):
                data = self.func(*args, **kwargs)
                return data
            return inner

        return wrapper

    def key_cache(self, expiration= 3600 * 24):
        """

        :param expiration:
        :return:
        """
        def wrapper(func):
            def inner(*args, **kwargs):
                data = self.func(*args, **kwargs)
                return data
            return inner
        return wrapper

    def acquire_lock(self, lock_name, acquire_timeout=10):
        """
        acquire lock
        :param lock_name:
        :param acquire_timeout:
        :return:
        """
        identifier = str(uuid.uuid4())
        end = time.time() + acquire_timeout
        while time.time() < end:
            if self.conn.setnx('lock:%s' % lock_name, identifier):
                return identifier
            time.sleep(0.001)
        return False

    def release_lock(self, lock_name, identifier):
        """
        release lock
        :param lock_name:
        :param identifier:
        :return:
        """
        pipe = self.conn.pipeline(True)
        lock_name = 'lock:%s' % lock_name

        while True:
            try:
                pipe.watch(lock_name)
                if pipe.get(lock_name) == identifier.encode('utf-8'):
                    pipe.multi()
                    pipe.delete(lock_name)
                    pipe.execute()
                    return True
                pipe.unwatch()
                break
            except redis.exceptions.WatchError:
                pass

        return False
