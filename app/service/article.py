from pickle import dumps as pickle_dumps
from pickle import loads as pickle_loads

from sqlalchemy import func

from app import redis
from app.models import Category, Tag, Post


@redis.hash_cache(key='category')
def fetch_category_list():
    """
    fetch category list
    :return:
    """
    return Category.query.all()


@redis.hash_cache(key='post')
def fetch_post_list():
    """
    fetch post list
    :return:
    """
    return Post.query.all()


def fetch_post(post_id):
    """
    fetch post by id
    :param post_id:
    :return:
    """
    data = redis.hget('post', post_id)
    if data:
        return pickle_loads(data)

    data = Post.query.filter(Post.id == post_id).first()
    if data:
        redis.hset('post', data.id, pickle_dumps(data))
    return data


@redis.hash_cache(key='tag')
def get_tag_list():
    return Tag.query.all()


def get_post_list_for_public():
    return Post.query.all()


def get_archive_list_of_post():
    q = Post.query
    q = q.group_by(func.date_format(Post.timestamp, '%Y%m'))
    q = q.with_entities(func.date_format(Post.timestamp, '%Y%m'),
                        func.count('*'))
    return q.all()
