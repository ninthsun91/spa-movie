import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Config(object):
    ENV = os.getenv("FLASK_DEBUG")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_COOKIE_NAME = "Toy Movie"

class devConfig(Config):
    # SERVER_NAME = "0.0.0.0"
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True