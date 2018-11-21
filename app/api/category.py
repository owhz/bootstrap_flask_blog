from flask import jsonify

from . import api_route
from app.models import Category


@api_route('/list', methods=['GET'])
def get_category_list():
    result = [{
        'name': i.name,
        'id': i.id
    } for i in Category.query.all()]
    return jsonify(result)
