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
    cover= request.args.get("cover")
    tag_id = request.args.get("tagId")

    return render_template("components/movieSearch.html",is_modal_covered=cover,tag_to_empty=tag_id)


@modals_ext.route("/upsert")
def upsert():
    # if login_check():
    #    abort(401)
    tag_to_empty = request.args.get("tagId")    

    return render_template("components/review_upsert.html",tag_to_empty=tag_to_empty,movie_title="tenet create",title="Make Review",make_edit="make") 


@modals_ext.route("/popup-upsertied")
def popup_upsertied():
    return render_template("components/popup.html",message="제출되었습니다")


@modals_ext.route("/edit")
def edit():
    # if login_check():
    #    abort(401)
    return render_template("components/review_upsert.html",movie_title="tenet edit",title="Edit Review",make_edit="edit")