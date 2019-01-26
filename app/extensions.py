from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_webpack import Webpack

from app.plugins.flask_redis import Redis
from app.plugins.flask_simplemde import SimpleMDE


db = SQLAlchemy()
moment = Moment()
bootstrap = Bootstrap()
login_manager = LoginManager()
simple_mde = SimpleMDE()
redis = Redis()
webpack = Webpack()

login_manager.login_view = 'auth.login'


def register_extensions(app):
    db.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    simple_mde.init_app(app)
    redis.init_app(app)
    webpack.init_app(app)
