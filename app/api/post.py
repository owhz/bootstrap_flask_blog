from flask import jsonify, request, abort
from sqlalchemy import and_

from app.models import Post, Category
from . import api_route


@api_route('/list', methods=['GET'])
def get_post_list():
    category_id = request.values.get('category_id', type=int)
    if category_id == 0:
        q = Post.query.filter(Post.is_public == True).all()
    else:
        q = Category.query.get(category_id)
        q = q.posts if q else []
    result = []
    if q:
        result = [{
            'title': i.title,
            'id': i.id
        } for i in q]
    return jsonify(result)


@api_route('/<int:id>', methods=['GET'])
def get_post_by_id(id):
    q = Post.query.filter(and_(Post.is_public == True,  Post.id == id)).first()
    if not q:
        abort(404)
    return jsonify({
        'title': q.title,
        'id': q.id,
        'body_html': q.body_html,
    })
