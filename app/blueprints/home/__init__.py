from flask import Blueprint


main_bp = Blueprint('home', __name__)


from . import views, errors
