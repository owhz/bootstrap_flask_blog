from flask import Blueprint


blog_bp = Blueprint('blog_bp', __name__)


from . import views
