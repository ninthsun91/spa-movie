from flask import Blueprint, render_template, request, jsonify
from ..config import Pymongo
from ..database import *


movie_bp = Blueprint("movie", __name__)
db = Pymongo.db


# 단일 영화 데이터 요청
@movie_bp.route("/movie", methods=["GET"])
def movie_view():
    """
    요청예시
        : GET, "/movie?code=999999"
        : code = 영화 code
    반환: movie(:dic)
        : movie = { code, image, title, director, actor, pubDate, naverRating,
                    userRating, description, reviews }
    """
    code = int(request.args["code"])
    movie = movie_code(code)

    return jsonify({ "movie": movie })


# 홈 메인 포스터 / 리뷰 최신 리뷰
@movie_bp.route("/recent")
@movie_bp.route("/recentrev")
def list_recent():
    """
    요청예시
        : GET, "/recent?page=page", "/recentrev?page=page"
        : page = 검색결과 페이지 넘버. 자연수
    반환
        : { movies|reviews, max_page }
        : 반환 원하는 필드는 아래 field 리스트에 기입
        : movies 전체필드 = [ "code", "title", "director", "actor", "pubDate",
                "naverRating", "userRating", "description", "reviews" ]

        : revies 전체필드 = [ "_id", "code", "username", "title", "comment",
                "userRating", "likes", "time" ]
        : max_page = 최대 페이지 수
    """
    # from /rev
    if "rev" in request.path:
        field = [ "_id", "code", "username", "title", "comment",
        "userRating", "likes", "time" ]
        result = review_card("recentrev", field, request.args)

        return jsonify( result )
    # from /
    else:
        field = [ "code", "title", "director", "actor", "pubDate",
                "naverRating", "userRating", "description", "reviews" ]
        result = movie_card("recent", field, request.args)

        return jsonify( result )


# 홈 최신 영화 목록
@movie_bp.route("/now")
def list_now():
    """
    요청예시
        : GET, "/now?page=page", 
        : page = 검색결과 페이지 넘버. 자연수
    반환
        : { movies: [Array(:dic, length=4)] }
        : 반환 원하는 필드는 아래 field 리스트에 기입
        : 전체필드 = [ "code", "title", "director", "actor", "pubDate",
                "naverRating", "userRating", "description", "reviews" ]
    """   
    field = [ "code", "title", "director", "actor", "pubDate", "naverRating" ]
    result = movie_card("now", field, request.args)

    return jsonify( result )


# 홈/리뷰 트랜딩 영화
@movie_bp.route("/trend")
@movie_bp.route("/trendrev")
def list_trend():
    """
    요청예시
        : GET, "/trend?page=page", "/trendrev?page=page"
        : page = 검색결과 페이지 넘버. 자연수
    반환
        : { movies: [Array(:dic, length=4/3)]}
        : 반환 원하는 필드는 아래 field 리스트에 기입
        : 전체필드 = [ "code", "title", "director", "actor", "pubDate",
                "naverRating", "userRating", "description", "reviews", "review_count" ]
        : review_cout = 리뷰 갯수
    """
    # from /rev
    if "rev" in request.path:
        field = [ "code", "title", "director", "actor", "pubDate", "naverRating" ]
        result = movie_card("trendrev", field, request.args)
    # from /
    else:
        field = [ "code", "title", "director", "actor", "pubDate", "naverRating" ]
        result = movie_card("trend", field, request.args)

    return jsonify( result )


# 영화 제목 검색
@movie_bp.route("/search")
def search_title():
    """
    요청예시
        : GET, "/search?page=page", 
        : page = 검색결과 페이지 넘버. 자연수
    반환
        : { result: [Array(:dic, length=max10)] }
        : 반환 원하는 필드는 아래 field 리스트에 기입
        : 전체필드 = [ "code", "title", "director", "actor", "pubDate",
                "naverRating", "userRating", "description", "reviews" ]
    """
    keyword = session.get("keyword")

    field = ["code", "image", "title", "director", "actor", "pubDate", "naverRating"]
    result = movies_title(field, keyword, page=request.args)
    
    return jsonify( result )






@movie_bp.route("/test2")
def test2():

    return ""

def test3(a):
    
    print(a["dir"])
    return ""
    


@movie_bp.route("/test", methods=["GET"])
def test():
   a = {
    "name": "kim",
    "birth": 1994,
    "skills": ["node.js", "python3"]
   }   
   return render_template("test.html", a=a)