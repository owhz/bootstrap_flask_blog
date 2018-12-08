from flask import jsonify

from app.service import article
from . import api_route


@api_route('/list', methods=['GET'])
def get_tag_list():
    data = article.fetch_tag_list()
    return jsonify([{'id': i.id, 'name': i.name} for i in data])
