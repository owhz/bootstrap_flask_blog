from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment

from .flask_redis import Redis
from .flask_simplemde import SimpleMDE
from config import config

db = SQLAlchemy()
moment = Moment()
bootstrap = Bootstrap()
login_manager = LoginManager()

simple_mde = SimpleMDE()
redis = Redis()

login_manager.login_view = 'auth.login'


def create_app(config_name):
    """
    factory function used for creating app
    :param config_name:
    :return:
    """

    app = Flask(__name__)
    config_obj = config[config_name]
    app.config.from_object(config_obj)
    config_obj.init_app(app)

    db.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    simple_mde.init_app(app)
    redis.init_app(app)

    from .main import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .user import user
    app.register_blueprint(user, url_prefix='/user')

    from .api import api
    app.register_blueprint(api, url_prefix='/api')

    return app
