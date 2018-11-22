from flask import jsonify

from . import api


@api.errorhandler(500)
def handle_internal_error(e):
    pass


@api.errorhandler(404)
def handle_not_found(e):
    pass
