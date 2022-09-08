from flask import Blueprint, render_template,request

components = Blueprint("components", __name__)

@components.route("/reviewcard")
def review_card():
   return render_template("components/review_card.html",movies=[1,2])

@components.route("/postercard-v")
def poster_card_v():
   return render_template("components/poster_card.html",movies=[1,2,3,4],direction="vertical")

@components.route("/postercard-h")
def poster_card_h():
   return render_template("components/poster_card.html",movies=[1,2,3,4],direction="horizontal")

@components.route("/signup")
def sign_up():
   tag_id = request.args.get("tagid")
   return render_template("components/sign_up.html",tag_to_empty=tag_id)

@components.route("/signin")
def sign_in():
   tag_id = request.args.get("tagid")
   return render_template("components/sign_in.html",tag_to_empty=tag_id)

@components.route("/moviesearch")
def create():
   cover= request.args.get("cover")
   tag_id = request.args.get("tagId")
   return render_template("components/movieSearch.html",is_modal_covered=cover,tag_to_empty=tag_id)

# @components.route("/moviesearch-uncov")
# def create_uncov():
#    return render_template("components/movieSearch.html",is_modal_covered=False)

@components.route("/upsert")
def upsert():
   return render_template("components/review_upsert.html",movie_title="tenet create",title="Make Review",make_edit="make") 

@components.route("/popup-upsertied")
def popup_upsertied():
   return render_template("components/popup.html",message="제출되었습니다")

@components.route("/view-review")
def view_review():
   tag_to_empty = request.args.get("tagId")
   return render_template("components/review.html",tag_to_empty=tag_to_empty)

@components.route("/edit")
def edit():
   print("edit")
   return render_template("components/review_upsert.html",movie_title="tenet edit",title="Edit Review",make_edit="edit")