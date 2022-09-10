from flask import Blueprint, render_template, request

from ..util import *


user_ext = Blueprint("user_ext", __name__)


user_ext.route("/signup")
def sign_up():
    tag_id = request.args.get("tagid")
    return render_template("components/sign_up.html",tag_to_empty=tag_id)


user_ext.route("/signin")
def sign_in():
    tag_id = request.args.get("tagid")
    return render_template("components/sign_in.html",tag_to_empty=tag_id)


user_ext.route("/profile/update")
def profile_update():
    tagId = request.args.get("tagId")
    user = users_uid()
    
    return render_template("components/profile.html", user=user, tagId=tagId)