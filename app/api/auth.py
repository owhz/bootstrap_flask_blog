from flask.views import View, MethodView, MethodViewType
from itsdangerous import TimedJSONWebSignatureSerializer

from . import api_route


@api_route('/login', methods=['GET', 'POST'])
def login():
    return ''
