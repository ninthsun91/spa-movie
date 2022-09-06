from email import message
from flask import Blueprint, render_template, jsonify, request

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
   return render_template("components/sign_up.html")

@components.route("/signin")
def sign_in():
   return render_template("components/sign_in.html")

@components.route("/plus/moviesearch")
def create():
   return render_template("components/movieSearch.html",is_modal_covered=True)

@components.route("/plus/moviesearch-uncov")
def create_uncov():
   return render_template("components/movieSearch.html",is_modal_covered=False)

@components.route("/upsert")
def upsert():
   return render_template("components/review_upsert.html",movie_title="tenet create",title="Make Review") 

@components.route("/popup-upsertied")
def popup_upsertied():
   return render_template("components/popup.html",message="제출되었습니다")

@components.route("/view-review")
def view_review():
   return render_template("components/review.html")

@components.route("/edit")
def edit():
   print("edit")
   return render_template("components/review_upsert.html",movie_title="tenet edit",title="Edit Review")