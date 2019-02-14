import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hard to guess'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_PORT = 6379

    BLOG_ADMIN_EMAIL = os.environ.get('BLOG_ADMIN_EMAIL') or 'admin@admin.com'
    BLOG_ADMIN_USERNAME = os.environ.get('BLOG_ADMIN_USERNAME') or 'admin'
    BLOG_ADMIN_NAME = os.environ.get('BLOG_ADMIN_NAME') or 'admin'
    BLOG_ADMIN_PASSWORD = os.environ.get('BLOG_ADMIN_PASSWORD') or 'admin'

    WEBPACK_MANIFEST_PATH = os.path.join(basedir, 'app/webpack/manifest.json')

    CELERY_RESULT_BACKEND = ''
    CELERY_BROKER_URL = ''

    @classmethod
    def init_app(cls, app):
        pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:%s@db/blog' % os.environ.get('DATABASE_PASSWORD')

    REDIS_URI = os.environ.get('REDIS_URI')

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
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/blog-dev'

    REDIS_URI = 'redis:@127.0.0.1'


class TestingConfig(Config):
    TESTING = True


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
