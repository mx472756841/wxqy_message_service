import logging.config
import os

from utils.log import Log

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SERVICE_NAME = "wx_message_service"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'v*Ri4eJYAUAjxkQ%jCJ$0ty1@cJa6o%BH@dEPDr%fJFSmi9tT12O36hHLRZQXGrh'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    UPLOAD_DIR = os.path.join(basedir, 'uploads')
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # 构建日志相关信息
    LOG_DIR = os.path.join(basedir, 'logs')
    if not os.path.isdir(LOG_DIR):
        os.mkdir(LOG_DIR)

    log = Log(LOG_DIR, SERVICE_NAME)
    logging.config.dictConfig(log.log_config_dict)

    # 缓存相关数据
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_PASS = ""
    REDIS_DB = 0

    #: 微信企业ID
    WX_CORPID = os.getenv("WX_CORPID") or "wx_corpid"
    #: 使用的企业微信中的应用ID
    DEFAULT_WX_AGENT_ID = os.getenv("DEFAULT_WX_AGENT_ID") or '1000002'
    #: 使用的企业微信中的应用的Secret
    WX_SECRET = os.getenv("WX_SECRET") or "wx_secret"
    # 可使用发送通知的Token,将符合的access_token配置到环境变量中  例如：123,456
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "").split(",") or []

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
