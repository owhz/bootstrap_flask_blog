import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hard to guess')
    BLOG_ADMIN_EMAIL = os.environ.get('BLOG_ADMIN_EMAIL', 'admin@example.com')
    BLOG_ADMIN_USERNAME = os.environ.get('BLOG_ADMIN_USERNAME', 'admin')
    BLOG_ADMIN_PASSWORD = os.environ.get('BLOG_ADMIN_PASSWORD', 'admin')

    @classmethod
    def init_app(cls, app):
        pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

    @classmethod
    def init_app(cls, app):
        import logging
        from logging import StreamHandler
        logger_handler = StreamHandler()
        logger_handler.setLevel(logging.INFO)
        app.logger.addHandler(logger_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        import logging
        from logging.handlers import SysLogHandler
        logger_handler = SysLogHandler()
        logger_handler.setLevel(logging.WARNING)
        app.logger.addHandler(logger_handler)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/bootstrap_blog'


class TestingConfig(Config):
    TESTING = True


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'unix': UnixConfig,
    'default': DevelopmentConfig
}
