from flask import Blueprint, render_template, session


home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    session["list_main"] = 0
    session["list_now"] = 0
    session["list_trend"] = 0
    return render_template("home.html")

@home_bp.route("/rev")
def review():
    return render_template("review_page.html")

@home_bp.route("/profile")
def profile():
   return render_template("my_page.html")
