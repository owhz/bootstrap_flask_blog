from flask import jsonify, request

from app.models import Post, Category
from . import api_route


@api_route('/list', methods=['GET'])
def get_post_list():
    category_id = request.values.get('category_id', type=int)
    if category_id == 0:
        q = Post.query.all()
    else:
        q = Category.query.get(category_id).posts
    result = []
    if q:
        result = [{
            'title': i.title,
            'id': i.id
        } for i in q]
    return jsonify(result)


@api_route('/<int:id>', methods=['GET'])
def get_post_by_id(id):
    q = Post.query.get_or_404(id)
    return jsonify({
        'title': q.title,
        'id': q.id,
        'body_html': q.body_html,
    })
