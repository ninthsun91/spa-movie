from flask import Blueprint, render_template, abort
from .config.session import *
from .database import user_uid, user_fill
from .util.cookie import *


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    initialize_home_session()
    if token_check() is None :
        return render_template("home.html", session="out")
    return render_template("home.html", session="in")


@main_bp.route("/rev")
def review():
    initialize_review_session()
    if token_check() is None :
        return render_template("review_page.html", session="out")
    return render_template("review_page.html", session="in")


@main_bp.route("/profile")
def profile():
    payload = token_check()
    if payload is None :
        abort(403)
    user = user_uid(payload["uid"])
    
    return render_template("my_page.html", user=user_fill(user), session="in")