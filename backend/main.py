from flask import Blueprint, render_template

from .config.session import *
from .util import *


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    initialize_home_session()
    return render_template("home.html")


@main_bp.route("/rev")
def review():
    initialize_review_session()
    return render_template("review_page.html")


@main_bp.route("/profile")
def profile():
    user = users_uid()
    return render_template("my_page.html", user=user)