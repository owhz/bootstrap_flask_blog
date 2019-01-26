from flask import Flask, render_template

from app.commands import register_commands
from app.extensions import register_extensions
from config import config


def register_blueprints(app):
    from .blueprints.main import main_bp
    from .blueprints.auth import auth_bp
    from .blueprints.user import user_bp
    from .blueprints.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(api_bp, url_prefix='/api')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_processor():
        pass


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        raise e
        # return render_template()

    @app.errorhandler(500)
    def internal_error(e):
        raise e


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

    register_commands(app)
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_errors(app)

    return app
