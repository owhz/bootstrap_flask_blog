from sqlalchemy import func

from app import redis
from app.models import Category, Tag, Post


@redis.hash_cache(key='category', field_finder=lambda x: x.id, expiration=3600 * 24)
def fetch_category_list():
    """
    fetch category list
    :return:
    """
    return Category.query.all()


@redis.hash_cache(key='post', field_finder=lambda x: x.id, expiration=3600 * 24)
def fetch_post(post_id):
    """
    fetch post by id
    :param post_id:
    :return:
    """
    return Post.query.filter(Post.id == post_id).first()


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
