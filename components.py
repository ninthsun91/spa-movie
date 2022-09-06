from flask import Blueprint, render_template, jsonify, request

components = Blueprint("components", __name__)

@components.route("/reviewcard")
def review_card():
   return render_template("components/review_card.html",movies=[1,2])

@components.route("/postercard")
def poster_card():
   return render_template("components/poster_card.html",movies=[1,2,3,4])

@components.route("/signup")
def components_sign_up():
   return render_template("components/sign_up.html")

@components.route("/signin")
def components_sign_in():
   return render_template("components/sign_in.html")