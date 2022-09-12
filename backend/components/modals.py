from flask import Blueprint, render_template, request
from ..database import *
from ..util import *


modals_ext = Blueprint("modals_ext", __name__)


@modals_ext.route("/signup")
def sign_up():
    tag_id = request.args.get("tagid")
    return render_template("components/sign_up.html",tag_to_empty=tag_id)


@modals_ext.route("/signin")
def sign_in():
    tag_id = request.args.get("tagid")
    return render_template("components/sign_in.html",tag_to_empty=tag_id)


@modals_ext.route("/profile/update")
def profile_update():
    tagId = request.args.get("tagId")
    payload = token_check()
    user = user_uid(payload["uid"])
    
    return render_template("components/profile.html", user=user, tag_to_empty=tagId)


@modals_ext.route("/moviesearch")
def create():
    if token_check() is None:
        return render_template("components/popup.html", message="리뷰를 작성하시려면 로그인해주세요")

    cover= request.args.get("cover")
    tag_id = request.args.get("tagId")

    return render_template("components/movieSearch.html",
        is_modal_covered=cover, tag_to_empty=tag_id)


@modals_ext.route("/popup")
def popup_msg():
    message = request.args.get("msg")
    return render_template("components/popup.html", message=message)


@modals_ext.route("/popup-review-create")
def popup_upsertied():
    type = request.args.get("type")
    print(type)
    if(type == "logout"):
        return render_template("components/popup.html", message="로그인 후 제출해주세요")
    if(type == "success"):
        return render_template("components/popup.html", message="리뷰가 제출 되었습니다.")


@modals_ext.route("/upsert")
def upsert():
    tag_to_empty = request.args.get("tagId")
    m_id = request.args.get("movieId")
    movie = movie_code(int(m_id))
    review = {
        "title": "",
        "comment": ""
    }
    
    return render_template("components/review_upsert.html", tag_to_empty=tag_to_empty, 
        movie=movie, review=review, title="Make Review", make_edit="make") 


@modals_ext.route("/edit")
def edit():
    tag_to_empty = request.args.get("tagId")    
    m_id = request.args.get("movieId")
    r_id = request.args.get("reviewId")
    movie = movie_code(int(m_id))
    review = review_id(r_id)

    return render_template("components/review_upsert.html", tag_to_empty=tag_to_empty,
        movie=movie, review=review, title="Edit Review", make_edit="edit", reviewId=r_id)