from flask import Flask

from .commands import register_commands
from .extensions import register_extensions
from wtforms.fields import HiddenField
from config import config


def register_blueprints(app):
    from .blueprints.home import main_bp
    from .blueprints.auth import auth_bp
    from .blueprints.user import user_bp
    from .blueprints.api import api_bp
    from .blueprints.admin import admin_bp
    from .blueprints.blog import blog_bp
    from .blueprints.post import post_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user/<username>')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(post_bp, url_prefix='/post')


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


def register_jinja_env_vars(app):
    app.jinja_env.globals['is_hidden_field'] = lambda x: isinstance(x, HiddenField)


def create_app(config_name):
    """
    Factory function used for creating app.
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

    register_jinja_env_vars(app)

    app.jinja_env.variable_start_string = '{@'
    app.jinja_env.variable_end_string = '@}'

    return app
