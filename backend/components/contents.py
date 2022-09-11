from flask import Blueprint, request, render_template
from ..database import *
from ..util import *


contents_ext = Blueprint("contents_ext", __name__)


@contents_ext.route("/postercard")
def poster_list():
    direction = request.args.get("direction")
    query = request.args.get("type")
    field = [ "code", "image", "title", "director", "actor", "pubDate", "naverRating" ]
    print("direction in posterlist:",direction)
    print("query in posterlist: ",query)
    if query == "search":
        keyword = request.args.get("keyword")
        result = movie_card("search", field, keyword=keyword)
        movies = result["movies"]
        max_page = result["max_page"]    
    else:        
        result = movie_card(query, field)
        movies = result["movies"]
        max_page = result["max_page"]

    return render_template("components/poster_card.html", movies=movies, direction=direction)


@contents_ext.route("/reviewcard")
def review_list():
    query = request.args.get("type")

    field = [ "_id", "code", "username", "title", "comment",
        "userRating", "likes", "time" ]
    result = review_card(query, field)
    reviews = result["reviews"]
    max_page = result["max_page"]

    for review in reviews:
        movie = movie_code(int(review["code"]))
        review["m_title"] = movie["title"]
        review["image"] = movie["image"]

    return render_template("components/review_card.html", reviews=reviews)


@contents_ext.route("/view-review")
def view_review():
    if(token_check()=="로그인 세션이 만료되었습니다."):
        return render_template("components/popup.html",message="리뷰를 확인하시려면 로그인해주세요")
    else:
        tag_to_empty = request.args.get("tagId")
        reviewid = request.args.get("reviewId")
        review_data = review_id(reviewid)
        movie = movie_code(review_data["code"])
        review_data["movie"] = movie
        review_data["likecount"] = len(review_data["likes"])
        print("review_data : ",review_data)
        return render_template("components/review.html",
            tag_to_empty=tag_to_empty, data=review_data)


@contents_ext.route("/movie-with-reviews")
def movie_with_reviews():
    print("hi")
    tag_to_empty = request.args.get("tagId")
    movieId = request.args.get("movieId")
    movie = movie_code(int(movieId))
    print("movie : ",movie)
    reviews = [review_id(reviewid) for reviewid in movie["reviews"]]

    return render_template("components/movie_with_reviews.html",
        tag_to_empty=tag_to_empty, movie=movie, reviews=reviews)
