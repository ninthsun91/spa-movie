from .env import Env


class Config(object):
    ENV = Env.DBG
    SECRET_KEY = Env.SKY
    SESSION_COOKIE_NAME = "Toy Movie"
    SESSION_COOKIE_HTTPONLY = False


class devConfig(Config):
    # SERVER_NAME = "0.0.0.0"
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True