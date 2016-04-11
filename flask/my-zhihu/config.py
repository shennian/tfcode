import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SERCET_KEY") or "i am secret key"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:sen1993@127.0.0.1:3306/my_zhihu'


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:kqf911@128.199.128.244/my_zhihu'


config = {
    "development": DevelopmentConfig,
    'test': TestConfig
}