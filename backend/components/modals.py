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
    user = user_uid()
    
    return render_template("components/profile.html", user=user, tag_to_empty=tagId)


@modals_ext.route("/moviesearch")
def create():
    if(token_check()=="로그인 세션이 만료되었습니다."):
        return render_template("components/popup.html",message="리뷰를 작성하시려면 로그인해주세요")
    else:
        cover= request.args.get("cover")
        tag_id = request.args.get("tagId")

        return render_template("components/movieSearch.html",is_modal_covered=cover,tag_to_empty=tag_id)


@modals_ext.route("/upsert")
def upsert():
    # if login_check():
    #    abort(401)
    tag_to_empty = request.args.get("tagId")    
    movie_id = request.args.get("movieId")
    movie = movie_code(int(movie_id))
    
    return render_template("components/review_upsert.html",tag_to_empty=tag_to_empty,movie=movie,movie_title="tenet create",title="Make Review",make_edit="make") 


@modals_ext.route("/popup-review-create")
def popup_upsertied():
    type = request.args.get("type")
    print(type)
    if(type == "logout"):
        return render_template("components/popup.html",message="로그인 후 제출해주세요")
    if(type == "success"):
        return render_template("components/popup.html",message="리뷰가 제출 되었습니다.")


@modals_ext.route("/edit")
def edit():
    # if login_check():
    #    abort(401)
    tag_to_empty = request.args.get("tagId")    
    movie_id = request.args.get("movieId")
    review_id = request.args.get("reviewId")
    print("review_id : ",review_id)
    movie = movie_code(int(movie_id))
    return render_template("components/review_upsert.html",tag_to_empty=tag_to_empty,movie=movie,title="Edit Review",make_edit="edit",review_id=review_id)