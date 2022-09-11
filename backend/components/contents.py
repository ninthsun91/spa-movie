from flask import Blueprint, request, render_template
from ..database import *
from ..util import *


contents_ext = Blueprint("contents_ext", __name__)


@contents_ext.route("/postercard")
def poster_list():
    """
    GET. 필요한 QS 데이터
    : direction = 포스터 표시 형식. horizontal | vertical
    : quert = 요청하는 컨텐츠 종류. recent | trend | trendrev | now
    """
    chevron_switch = request.args.get("chevron")
    direction = request.args.get("direction")
    query = request.args.get("query")
    field = [ "code", "image", "title", "director", "actor", "pubDate", "naverRating" ]

    if query == "search":
        keyword = request.args.get("keyword")
        result = movie_card("search", field, keyword=keyword)
        movies = result["movies"]
        max_page = result["max_page"]    
    else:        
        result = movie_card(query, field)
        movies = result["movies"]
        max_page = result["max_page"]

    return render_template("components/poster_card.html",
        movies=movies, direction=direction, query=query,chevron=chevron_switch)


@contents_ext.route("/reviewcard")
def review_list():
    """
    GET. 필요한 QS 데이터
    : query = 요청하는 컨텐츠 종류. popular | recentrev
    """
    query = request.args.get("query")

    field = [ "_id", "code", "username", "title", "comment",
        "userRating", "likes", "time" ]
    result = review_card(query, field)
    reviews = result["reviews"]
    max_page = result["max_page"]

    for review in reviews:
        movie = movie_code(int(review["code"]))
        review["m_title"] = movie["title"]
        review["image"] = movie["image"]

    return render_template("components/review_card.html",
        reviews=reviews, query=query, max_page=max_page)


@contents_ext.route("/view-review")
def view_review():
    if token_check() is None:
        return render_template("components/popup.html",message="리뷰를 확인하시려면 로그인해주세요")

    tag_to_empty = request.args.get("tagId")
    reviewid = request.args.get("reviewId")
    review_data = review_id(reviewid)
    movie = movie_code(review_data["code"])
    review_data["movie"] = movie
    review_data["likecount"] = len(review_data["likes"])

    return render_template("components/review.html",
        tag_to_empty=tag_to_empty, data=review_data)


@contents_ext.route("/movie-with-reviews")
def movie_with_reviews():
    tag_to_empty = request.args.get("tagId")
    movieId = request.args.get("movieId")
    movie = movie_code(int(movieId))
    reviews = [review_id(reviewid) for reviewid in movie["reviews"]]
    print("reviews : ",reviews)
    print("hi")

    return render_template("components/movie_with_reviews.html",
        tag_to_empty=tag_to_empty, movie=movie, reviews=reviews)
