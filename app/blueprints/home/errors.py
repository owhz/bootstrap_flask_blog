from flask import render_template

from . import home_bp


@home_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@home_bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 505
