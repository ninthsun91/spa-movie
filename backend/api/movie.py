from flask import Blueprint, render_template, request, jsonify

from ..config import *
from ..util import *


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
    movie = movies_code(code)

    return jsonify({ "movie": movie })


# 홈 메인 포스터 / 리뷰 최신 리뷰
@movie_bp.route("/recent")
@movie_bp.route("/recentrev")
def list_recent():
    """
    요청예시
        : GET, "/recent?dir=left" or "/rev/recent?page=3"
        : dir = left | right, page = 1 이상의 자연수
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
        : GET, "/now?dir=right"
        : dir = left | right
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
        : GET, "/trend?dir=left" or "/rev/trend?dir=right"
        : dir = left | right
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
@movie_bp.route("/search", methods=["POST"])
def search_title():
    """
    요청예시
        : POST, "/search", data={ keyword(:str) }
        : keyword = 검색어
    반환
        : { result: [Array(:dic, length=max10)] }
        : 반환 원하는 필드는 아래 field 리스트에 기입
        : 전체필드 = [ "_id", "code", "title", "director", "actor", "pubDate",
                "naverRating", "userRating", "description", "reviews" ]
    """
    keyword = request.form["keyword"]

    search_naver(keyword)
    field = ["code", "image", "title", "director", "actor", "pubDate", "naverRating"]
    movies = movie_field(movies_title(keyword, 10), field)

    return jsonify({ "result": movies })




@movie_bp.route("/rev/test2")
@movie_bp.route("/test2")
def test2():
    test3(request.args)

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


# 네이버 영화DB 스크랩 -> DB 유지관리용. 웹사이트에는 사용 안될거에요
@movie_bp.route("/scrap", methods=["GET"])
def scrap():
    print("scrap")

    from bs4 import BeautifulSoup
    import requests

    url = "https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&tg=0&date=20220901"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # #old_content > table > tbody > tr:nth-child(2) > td.title
    body = soup.select_one("#old_content > table > tbody")
    # old_content > table > tbody > tr:nth-child(2) > td.title > div > a
    tags = body.select("tr > td.title > div > a")
    for tag in tags:
        title = tag["title"]
        code = int(tag["href"].split("code=")[1])

        naver = search_naver(title)[0]

        url = f"https://movie.naver.com/movie/bi/mi/basic.naver?code={code}"
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        desc = soup.select_one("#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p")
        pubDate = soup.select_one("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4)")
                                   #content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3) > a:nth-child(1)
                                   #content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)
        movie = {
            "code": code,
            "image": naver["image"],
            "title": title,
            "director": naver["director"],
            "actor": naver["actor"],
            "pubDate": remove_tags(str(pubDate)).strip().replace("\n", "")[0:10],
            "naverRating": naver["naverRating"],
            "userRating": "0.00",
            "description": remove_tags(str(desc)),
            "reviews": [],
        }
        find = db.movies.find_one({"code": code})
        # print(movie)
        if find is None:
            print(f"{title} None")
            db.movies.insert_one(movie)
        else:
            print(f"{title} Exists")

    return ""
