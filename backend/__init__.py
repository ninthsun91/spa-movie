from flask import Flask, render_template
from .config import config


def router(flask_app: Flask):
   from .main import main_bp
   from .components import components_bp
   from .api import movie_bp, review_bp, user_bp

   flask_app.register_blueprint(main_bp)
   flask_app.register_blueprint(components_bp, url_prefix="/components")
   flask_app.register_blueprint(movie_bp)
   flask_app.register_blueprint(review_bp)
   flask_app.register_blueprint(user_bp)

   @flask_app.errorhandler(403)
   def forbidden_403(e):
      return render_template("others/403.html"), 403

   @flask_app.errorhandler(404)
   def page_not_found_404(e):
      return render_template("others/404.html"), 404


def create_app():
   app = Flask(__name__,
      template_folder="../frontend/templates", static_folder="../frontend/static")
   app.config.from_object((flask_env()))
   router(app)

   return app


def flask_env():
   if config.Config.ENV=="development":
      print("development")
      return "backend.config.config.devConfig"
   else:
      print("production")
      return "backend.config.config.Config"

