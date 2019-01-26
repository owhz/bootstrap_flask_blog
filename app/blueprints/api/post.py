from flask import abort, jsonify, request
from sqlalchemy import and_

from app.models import Category, Post
from app.service import article

from . import api_route


@api_route('/list', methods=['GET'])
def get_post_list():
    category_id = request.values.get('category_id', type=int)
    if category_id == 0:
        # q = Post.query.filter(Post.is_public == True).all()
        data = article.fetch_post_list()
    else:
        # q = Category.query.get(category_id).posts
        data = article.fetch_post_list_of_category(category_id)
    result = []
    if data:
        result = [{'title': i.title, 'id': i.id} for i in data]
    return jsonify(result)


@api_route('/<int:id>', methods=['GET'])
def get_post_by_id(id):
    data = article.fetch_post(id, False)
    if not data:
        abort(404)
    return jsonify({
        'title': data.title,
        'id': data.id,
        'body_html': data.body_html,
    })
