from flask import Blueprint, render_template

from .config.session import *
from .util import *


home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    initialize_home_session()
    return render_template("home.html")


@home_bp.route("/rev")
def review():
    initialize_review_session()
    return render_template("review_page.html")


@home_bp.route("/profile")
def profile():
    user = users_uid()
    return render_template("my_page.html", user=user)