from flask import Blueprint


blog_bp = Blueprint('blog', __name__)


from . import views
