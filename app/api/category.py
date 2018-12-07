from flask import jsonify

from . import api_route

from app.service import article


@api_route('/list', methods=['GET'])
def get_category_list():

    result = article.fetch_category_list()
    return jsonify([{ 'name': i.name, 'id': i.id } for i in result])
