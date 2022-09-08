from flask import Blueprint, render_template, request, jsonify, session
from ordered_set import OrderedSet

from ..config import *
from ..util import *


movie_bp = Blueprint("movie", __name__)
db = Pymongo.db


# 단일 영화 데이터 요청
@movie_bp.route("/movie", methods=["GET"])
def movie_view():
    """
    요청예시: GET, "/movie?code=999999"
    code = 영화 code
    반환: movie(:dic)
        movie = { code, image, title, director, actor, pubDate, naverRating,
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
    요청예시: GET, "/recent?dir=left" or "/rev/recent?page=3"
        dir = left | right, page = 1 이상의 자연수
    반환: "/recent"     >   movie
            movie = { code, image, title, director, actor, pubDate,
                        naverRating, userRating, description, reviews }
          "/recentrev" >   { reviews: [Array(:dic, length=2)], max_page: max_page(:int) }
            arry dic = { _id, code, username, title, comment, userRating, likes, time }
            max_page = 최대 페이지 수 (전체리뷰 / 2)
    """
    reviews = reviews_time()

    # from /rev
    if "rev" in request.path:
        if "page" in request.args:
            page = int(request.args["page"])
            session["review_recent"] = page        
        else:
            page = session.get("review_recent")
        skip = (page-1) * 2
        max_page = int(len(reviews) / 2)

        return jsonify({ "reviews": reviews[skip:skip+2], "max_page": max_page })
    # from /
    else:
        if "dir" in request.args:
            dir = request.args["dir"]
            if dir=="right":
                dir = request.args["dir"]
                session["list_recent"] += 1
            elif dir=="left":
                dir = request.args["dir"]
                session["list_recent"] -= 1    
        if abs(session.get("list_recent"))==3:
                session["list_recent"] = 0
        page = session.get("list_recent")
        skip = page if page>=0 else 3 + page
        
        codes = OrderedSet()
        for review in reviews:
            codes.add(review["code"])
            if len(codes)==3:
                break
        code = list(codes)[skip]

        return jsonify({ "movie": movies_code(code) })


# 홈 최신 영화 목록
@movie_bp.route("/now")
def list_now():
    """
    요청예시: GET, "/now?dir=right"
    dir = left | right
    반환: { movies: [Array(:dic, length=4)] }
        dic = { code, image, title, director, actor, pubDate, naverRating }
    """
    if "dir" in request.args:
        dir = request.args["dir"]
        if dir=="right":
            dir = request.args["dir"]
            session["list_now"] += 1
        elif dir=="left":
            dir = request.args["dir"]
            session["list_now"] -= 1 
    if abs(session.get("list_now"))==10:
        session["list_now"] = 0
    page = session.get("list_now")
    skip = page if page>=0 else 10 + page
    skip = (page * 4) if page>=0 else (40 + (page * 4))

    movies = movies_pubDate(40, skip)
    movies = movies[0:4]
    for movie in movies:
        [movie.pop(key) for key in ["userRating", "description", "reviews"]]

    return jsonify({ "movies": movies })


# 홈/리뷰 트랜딩 영화
@movie_bp.route("/trend")
@movie_bp.route("/trendrev")
def list_trend():
    """
    요청예시: GET, "/trend?dir=left" or "/rev/trend?dir=right"
        dir = left | right
    반환: { movies: [Array(:dic, length=4/3)]}
        dic = { code, image, title, director, actor, pubDate, userRating, review_count}
        review_cout = 리뷰 갯수
    """
    # from /rev
    if "rev" in request.path:
        if "dir" in request.args:
            dir = request.args["dir"]
            if dir=="right":
                dir = request.args["dir"]
                session["review_trend"] += 1
            elif dir=="left":
                dir = request.args["dir"]
                session["review_trend"] -= 1 
        if abs(session.get("review_trend"))==10:
            session["review_trend"] = 0
        page = session.get("review_trend")
        skip = page if page>=0 else 10 + page
        skip = (page * 3) if page>=0 else (30 + (page * 3))

        movies = movies_rcount(30, skip)
        movies = movies[0:3]
        for movie in movies:
            [movie.pop(key) for key in ["naverRating", "description", "reviews"]]
            
        return jsonify({ "movies": movies })
    # from /
    else:
        if "dir" in request.args:
            dir = request.args["dir"]
            if dir=="right":
                dir = request.args["dir"]
                session["list_trend"] += 1
            elif dir=="left":
                dir = request.args["dir"]
                session["list_trend"] -= 1 
        if abs(session.get("list_trend"))==10:
            session["list_trend"] = 0
        page = session.get("list_trend")
        skip = page if page>=0 else 10 + page
        skip = (page * 4) if page>=0 else (40 + (page * 4))

        movies = movies_rcount(40, skip)
        movies = movies[0:4]
        for movie in movies:
            [movie.pop(key) for key in ["naverRating", "description", "reviews"]]
            
        return jsonify({ "movies": movies })


# 영화 제목 검색
@movie_bp.route("/search", methods=["POST"])
def search_title():
    """
    요청예시: POST, "/search", data={ keyword(:str) }
    keyword = 검색어
    반환: { result: [Array(:dic, length=max20)] }
        dic = { code, title, director, actor, pubDate }
    """
    keyword = request.form["keyword"]

    naver = search_naver(keyword)    
    for n in naver:
        [n.pop(key) for key in ["image", "naverRating"]]
    db = movies_title(keyword, 10)
    for d in db:
        [d.pop(key) for key in ["_id", "image", "naverRating", "userRating",
                                    "description", "reviews"]]

    return jsonify({ "result": db + naver })



@movie_bp.route("/rev/test2")
@movie_bp.route("/test2")
def test2():
    return ""

def test3(a :int):    
    print(a)


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
