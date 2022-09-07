from flask import Flask
from .config import config


def router(flask_app: Flask):
   from .home import home_bp
   from .components import components
   from .api.movie import movie_bp
   from .api.review import review_bp
   from .api.user import user_bp

   flask_app.register_blueprint(home_bp, url_prefix="/")
   flask_app.register_blueprint(components, url_prefix="/components")
   flask_app.register_blueprint(movie_bp, url_prefix="/")
   flask_app.register_blueprint(review_bp, url_prefix="/")
   flask_app.register_blueprint(user_bp, url_prefix="/")


def create_app():
   app = Flask(__name__,
      template_folder="../frontend/templates", static_folder="../frontend/static")
   app.config.from_object((flask_env()))
   router(app)

   return app


def flask_env():
   if config.Config.ENV=="development":
      return "backend.config.config.devConfig"
   else:
      return "backend.config.config.Config"