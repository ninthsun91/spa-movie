from flask import Blueprint, render_template, request

from ..util import *


review_ext = Blueprint("review_ext", __name__)


@review_ext.route("/reviewcard")
def review_list():
    query = request.args.get("type")

    field = [ "_id", "code", "username", "title", "comment",
        "userRating", "likes", "time" ]
    result = review_card(query, field)
    reviews = result["reviews"]
    max_page = result["max_page"]

    return render_template("components/review_card.html", reviews=reviews)


# def review_card():
#     type = request.args.get("type")
#     if type=="recent" :
#         reviews = reviews_time()
#         for index, review in enumerate(reviews) :
#             print(review)
#             movie = movies_code(review["code"])
#             reviews[index]["movie"] = movie
#     elif type=="popular" : 
#         reviews = reviews_likes()
#         for index, review in enumerate(reviews) :
#             print(review)
#             movie = movies_code(review["code"])
#             reviews[index]["movie"] = movie

#     return render_template("components/review_card.html", reviews=reviews)


@review_ext.route("/moviesearch")
def create():
    cover= request.args.get("cover")
    tag_id = request.args.get("tagId")

    return render_template("components/movieSearch.html",is_modal_covered=cover,tag_to_empty=tag_id)


@review_ext.route("/upsert")
def upsert():
    # if login_check():
    #    abort(401)
    tag_to_empty = request.args.get("tagId")    

    return render_template("components/review_upsert.html",tag_to_empty=tag_to_empty,movie_title="tenet create",title="Make Review",make_edit="make") 


@review_ext.route("/popup-upsertied")
def popup_upsertied():
    return render_template("components/popup.html",message="제출되었습니다")


@review_ext.route("/view-review")
def view_review():
    tag_to_empty = request.args.get("tagId")
    review_id = request.args.get("reviewId")
    review_data = reviews_id(review_id)
    movie = movies_code(review_data["code"])
    review_data["movie"] = movie
    review_data["likecount"] = len(review_data["likes"])

    return render_template("components/review.html",tag_to_empty=tag_to_empty,data=review_data)


@review_ext.route("/edit")
def edit():
    # if login_check():
    #    abort(401)
    return render_template("components/review_upsert.html",movie_title="tenet edit",title="Edit Review",make_edit="edit")


@review_ext.route("/movie-with-reviews")
def movie_with_reviews():
    tag_to_empty = request.args.get("tagId")
    movieId = request.args.get("movieId")
    movie = movies_code(int(movieId))
    reviews = [reviews_id(review_id) for review_id in movie["reviews"]]

    return render_template("components/movie_with_reviews.html",tag_to_empty=tag_to_empty,movie=movie,reviews=reviews)