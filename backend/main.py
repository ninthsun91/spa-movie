from flask import Blueprint, render_template

from .config.session import *
from .database import user_uid
from .util import *

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    initialize_home_session()
    if(token_check() == "로그인 세션이 만료되었습니다.") :
        return render_template("home.html",session="out")
    else :
        return render_template("home.html",session="in")
        

@main_bp.route("/rev")
def review():
    initialize_review_session()
    return render_template("review_page.html")


@main_bp.route("/profile")
def profile():
    user = user_uid()
    return render_template("my_page.html", user=user)