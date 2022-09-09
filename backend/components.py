from flask import Blueprint, render_template,request

from .util import *
from .api.review import *


components = Blueprint("components", __name__)

@components.route("/reviewcard")
def review_card():
    reviews = reviews_time()
    for index, review in enumerate(reviews) :
        movie = movies_code(review["code"])
        reviews[index]["movie"] = movie
    return render_template("components/review_card.html",reviews=reviews)

@components.route("/postercard")
def poster_card():
    direction = request.args.get("direction")
    count = int(request.args.get("count"))
    movies = movies_pubDate(40)
    movies = movies[0:count]
    for movie in movies:
        [movie.pop(key) for key in ["userRating", "description", "reviews"]]
    return render_template("components/poster_card.html",movies=movies,direction=direction)


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

@components.route("/upsert")
def upsert():
    # if login_check():
    #    abort(401)
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
    # if login_check():
    #    abort(401)
    return render_template("components/review_upsert.html",movie_title="tenet edit",title="Edit Review",make_edit="edit")