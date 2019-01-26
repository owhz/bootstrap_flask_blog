import base64

import redis

from . import api_bp


redis = redis.Redis(host='host', port=6379)


@api_bp.route('/image', methods=['POST'])
def upload_image():
    pass


@api_bp.route('/image', methods=['GET'])
def get_image():
    pass


@api_bp.route('/image', methods=['DELETE'])
def delete_image():
    pass
