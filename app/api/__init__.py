import re

from flask import Blueprint
from flask._compat import with_metaclass

from flask.views import View, MethodView

MODULE_NAME_REGEX = re.compile(r'app\.api\.')

api = Blueprint('api', __name__)


@api.after_request
def after_request(response):
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,OPTIONS,PUT'
    # response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    # response.headers['Access-Control-Max-Age'] = '1800'
    return response


class ApiViewType(type):
    def __new__(mcls, name, *bases, **attrs):
        return type.__new__(mcls, name, *bases, **attrs)

    def __init__(cls, name, *bases, **attrs):
        super(ApiViewType, cls).__init__(name, *bases, **attrs)


class ApiView(with_metaclass(ApiViewType, View)):
    def dispatch_request(self, *args, **kwargs):
        pass


def api_route(rule=None, **options):
    def decorator(func):
        nonlocal rule
        rule_prefix = get_rule_prefix(func.__module__)
        if not rule:
            rule = '/%s/%s' % (rule_prefix, func.__name__)
        else:
            assert rule.startswith('/') is True, 'The rule should start with \'/\'.'
            rule = '/%s%s' % (rule_prefix, rule)
        endpoint = options.pop("endpoint", func.__name__)
        add_url_rule(rule, endpoint, func, **options)
        return func

    def get_rule_prefix(func_module):
        _, name = MODULE_NAME_REGEX.split(func_module)
        return name.replace('.', '/') if '.' in name else name

    def add_url_rule(rule, endpoint, func, **options):
        api.add_url_rule(rule, endpoint, func, **options)

    return decorator


from . import auth, image, post, user, tag, category
