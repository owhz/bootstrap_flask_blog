from flask import jsonify

from . import api_bp


@api_bp.errorhandler(500)
def handle_internal_error(e):
    pass


@api_bp.errorhandler(404)
def handle_not_found(e):
    pass
