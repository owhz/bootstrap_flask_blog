from flask.views import MethodView, MethodViewType, View
from itsdangerous import TimedJSONWebSignatureSerializer

from . import api_route


@api_route('/login', methods=['GET', 'POST'])
def login():
    return ''
