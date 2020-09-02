class Config(object):
    DEBUG = False
    TESTING = False
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/zhongtuo_flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 设置session密钥
    SECRET_KEY = 'secret_key'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/zhongtuo_flask'


class DevelopmentConfig(Config):
    DEBUG = True
    # 静态资源加载问题
    # 方式一
    # app.jinja_env.auto_reload = True
    # 方式二每五秒请求静态资源
    # from datetime import timedelta
    # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


class TestingConfig(Config):
    TESTING = True