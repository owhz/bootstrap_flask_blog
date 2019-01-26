from pickle import dumps as pickle_dumps
from pickle import loads as pickle_loads

from sqlalchemy import func

from app.extensions import redis
from app.models import Category, Post, Tag


@redis.hash_cache(key_name='category', expiration=None)
def fetch_category_list():
    """
    fetch category list
    :return:
    """
    data = Category.query.all()

    with redis.pipeline(True) as pipeline:
        #pipeline.watch()
        pipeline.multi()
        for i in data:
            ids = [j.id for j in i.posts]
            if ids:
                pipeline.sadd('category:%d:posts' % i.id, *ids)
        pipeline.execute()
    return data


@redis.hash_cache(key_name='post', expiration=None)
def fetch_post_list():
    """
    fetch post list
    :return:
    """
    data = Post.query.filter(Post.is_public == True).all()

    with redis.pipeline(True) as pipeline:
        #pipeline.watch()
        pipeline.multi()
        for i in data:
            pipeline.sadd('post:%d:category' % i.id, i.category_id)
        pipeline.execute()
    return data


@redis.hash_cache(key_name='tag', expiration=None)
def fetch_tag_list():
    data = Tag.query.all()
    return data


def fetch_post(post_id, is_public):
    """
    fetch post by id
    :param is_public:
    :param post_id:
    :return:
    """
    data = redis.hget('post', post_id)
    if data:
        data = pickle_loads(data)
    else:
        data = Post.query.filter(Post.id == post_id, Post.is_public == is_public).first()
        if data:
            redis.hset('post', data.id, pickle_dumps(data))
    return data


def get_archive_list_of_post():
    q = Post.query
    q = q.group_by(func.date_format(Post.timestamp, '%Y%m'))
    q = q.with_entities(func.date_format(Post.timestamp, '%Y%m'),
                        func.count('*'))
    return q.all()


def fetch_post_list_of_category(category_id):
    pass


def fetch_category(category_id):
    data = redis.hget('category', category_id)

    if data:
        return pickle_loads(data)
    else:
        pass
