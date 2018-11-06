import base64

import redis

from . import api


@api.route('/image', methods=['POST'])
def upload_image():
    pass


@api.route('/image', methods=['GET'])
def get_image():
    pass


@api.route('/image', methods=['DELETE'])
def delete_image():
    pass
