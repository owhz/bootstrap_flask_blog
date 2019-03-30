from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_webpack import Webpack
from flask_socketio import SocketIO
from flask_io import FlaskIO

from app.plugins.flask_redis import Redis
from app.plugins.flask_simplemde import SimpleMDE


db = SQLAlchemy()
login_manager = LoginManager()
redis = Redis()
webpack = Webpack()
socketio = SocketIO()
flaskio = FlaskIO()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    redis.init_app(app)
    webpack.init_app(app)
    socketio.init_app(app)
    # flaskio.init_app(app)
