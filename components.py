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

@components.route("/plus/create")
def create():
   return render_template("components/plus/create.html")