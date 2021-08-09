import os
from datetime import timedelta
from pathlib import Path


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES")))
    WEB_SECRET_KEY = os.getenv("WEB_SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    CORS_ENABLED = True
    #
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": int(os.getenv("DATABASE_POOL_RECYCLE") or "90"),
        "pool_timeout": int(os.getenv("DATABASE_POOL_TIMEOUT") or "900"),
        "pool_size": int(os.getenv("DATABASE_POOL_SIZE") or "10"),
        "max_overflow": int(os.getenv("DATABASE_MAX_OVERFLOW") or "5"),
    }

    # filename = os.getenv("LOG_FILE") or "server" #TODO maybe can delete

    # absolute path for safety
    # LOG_FILE = Path(Path.cwd(), "logs", f"{filename}.log")
    # path = LOG_FILE.parent
    path = Path(Path.cwd(), "logs")
    if not (path.exists() and path.is_dir()):
        Path.mkdir(path)


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class HerokuConfig(Config):
    DEBUG = False
    TESTING = False


__config_list = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    heroku=HerokuConfig
)


def get_config(config_name):
    return __config_list.get(config_name, DevelopmentConfig)


jwt_key = Config.JWT_SECRET_KEY
