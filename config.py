import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hard to guess'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BLOG_ADMIN_EMAIL = os.environ.get('BLOG_ADMIN_EMAIL') or 'admin@admin.com'
    BLOG_ADMIN_USERNAME = os.environ.get('BLOG_ADMIN_USERNAME') or 'admin'
    BLOG_ADMIN_NAME = os.environ.get('BLOG_ADMIN_NAME') or 'admin'
    BLOG_ADMIN_PASSWORD = os.environ.get('BLOG_ADMIN_PASSWORD') or 'admin'

    @classmethod
    def init_app(cls, app):
        pass


class ProductionConfig(Config):
    DATABASE_PASSWORD  = os.environ['DATABASE_PASSWORD']
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:%s@db/blog' % DATABASE_PASSWORD

    @classmethod
    def init_app(cls, app):
        import logging
        from logging import StreamHandler
        logger_handler = StreamHandler()
        logger_handler.setLevel(logging.INFO)
        app.logger.addHandler(logger_handler)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/blog'


class TestingConfig(Config):
    TESTING = True


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
