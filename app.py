from flask import Flask, render_template, session
from dotenv import load_dotenv
import os

from components import components
from movie import movie_bp
from review import review_bp
from user import user_bp


load_dotenv()
KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)
app.config.update(
   SECRET_KEY=KEY,
   SESSION_COOKIE_NAME = "home_movie_list",
   TEMPLATES_AUTO_RELOAD=True
)

app.register_blueprint(components, url_prefix="/components")
app.register_blueprint(movie_bp, url_prefix="/")
app.register_blueprint(review_bp, url_prefix="/")
app.register_blueprint(user_bp, url_prefix="/")


@app.route("/")
def home():
   session["list_main"] = 0
   session["list_now"] = 0
   session["list_trend"] = 0
   return render_template("home.html")
@app.route("/rev")
def review():
   return render_template("review_page.html")

if __name__ == "__main__":
   app.run("0.0.0.0", port=5000, debug=True)
