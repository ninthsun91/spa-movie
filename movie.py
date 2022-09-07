from flask import Blueprint, render_template, request, jsonify, session
from pymongo import MongoClient

import urllib.request
import json
import os
from dotenv import load_dotenv
from ordered_set import OrderedSet

from bs4 import BeautifulSoup
import requests

from regex import *

load_dotenv()
URL = os.environ.get("MongoDB_URL")
NMV = os.environ.get("NMovie_Search")
CID = os.environ.get("Client_ID")
CSC = os.environ.get("Client_Secret")

client = MongoClient(URL, tls=True, tlsAllowInvalidCertificates=True)
db = client.spamovie

movie_bp = Blueprint("movie", __name__)


# 홈화면 메인 포스터
@movie_bp.route("/carousel")
def movie_carousel():
    dir = request.args["dir"]
    if dir=="right":
        session["list_main"] += 1
    elif dir=="left":
        session["list_main"] -= 1    
    if abs(session.get("list_main"))==10:
        session["list_main"] = 0
    page = session.get("list_main")
    skip = page if page>=0 else 10 + page

    pipeline = [
        {
            "$sort": {"time": -1}
        }, {
            "$project": {
                "_id": 0,
                "code": 1,
                "title": 1,
                "time": 1,
            }
        }, {"$limit": 50}
    ]
    review_search = db.reviews.aggregate(pipeline)
    
    codes = OrderedSet()
    for review in review_search:
        codes.add(review["code"])
        if len(codes)==10:
            break

    code = list(codes)[skip]
    movie = db.movies.find_one({"code": code}, {"_id": False})

    return jsonify({ "movie": movie })


# 홈화면 최신 영화 목록
@movie_bp.route("/movienow")
def movie_now():
    print(session)
    dir = request.args["dir"]
    if dir=="right":
        session["list_now"] += 1
    elif dir=="left":
        session["list_now"] -= 1    
    if abs(session.get("list_now"))==10:
        session["list_now"] = 0
    page = session.get("list_now")
    skip = page if page>=0 else 10 + page
    skip = (page * 4) if page>=0 else (40 + (page * 4))

    pipeline = [
        {
            "$search": {
                "index": "movie_title",
                "regex": {
                    "query": "[0-9.]{4,10}",
                    "path": "pubDate",
                    "allowAnalyzedField": True
                }
            }
        }, {
            "$sort": { "pubDate": -1 }
        }, {
            "$project": {
                "_id": 0,
                "code": 1,
                "image": 1,
                "title": 1,
                "director": 1,
                "actor": 1,
                "pubDate": 1,
                "naverRating": 1,
            }
        }, {"$limit": 40}, {"$skip": skip}
    ]
    movies_search = db.movies.aggregate(pipeline)

    movies = []
    for movie in movies_search:
        movies.append(movie)

    return jsonify({ "movies": movies[0:4] })


# 홈화면 트랜딩 영화 목록
@movie_bp.route("/movietrend")
def movie_trend():
    dir = request.args["dir"]
    if dir=="right":
        session["list_trend"] += 1
    elif dir=="left":
        session["list_trend"] -= 1
    if abs(session.get("list_trend"))==10:
        session["list_trend"] = 0
    page = session.get("list_trend")
    skip = page if page>=0 else 10 + page
    skip = (page * 4) if page>=0 else (40 + (page * 4))

    pipeline = [
        {
            "$project": {
                "_id": 0,
                "code": 1,
                "image": 1,
                "title": 1,
                "director": 1,
                "actor": 1,
                "pubDate": 1,
                "naverRating": 1,
                "review_count": {"$size": "$reviews"}
            }
        }, {
            "$sort": {
                "review_count": -1,
                "naverRating": -1
            }
        }, {"$limit": 40}, {"$skip": skip}
    ]
    movies_search = db.movies.aggregate(pipeline)

    movies = []
    for movie in movies_search:
        movies.append(movie)
        
    return jsonify({ "movies": movies[0:4] })


# 영화 상세
@movie_bp.route("/movie", methods=["GET"])
def movie_view():
   code = int(request.args["code"])
   movie = db.movies.find_one({"code": code}, {"_id": False})
   
   return render_template("movie.html", movie=movie)


# 영화 제목 검색
@movie_bp.route("/search", methods=["POST"])
def search_title():
    keyword = request.form["keyword"]

    naver = search_naver(keyword)    
    for n in naver:
        n.pop("image")
        n.pop("naverRating")
    result = search_db(keyword) + naver

    return jsonify({ "result": result })


# MongoDB 제목 검색
def search_db(keyword):
   pipeline = [
      {
        "$search": {
            "index": "movie_title",
            "text": {
                "query": keyword,
                "path": "title",
            }
        }
      }, {
         "$project": {
            "_id": 0,
            "code": 1,
            "title": 1,
            "director": 1,
            "actor": 1,
            "pubDate": 1,
         }
        }
   ]
   movies = db.movies.aggregate(pipeline)
   result = []
   for movie in movies:
      result.append(movie)
   return result


# 네이버영화 검색 API
def search_naver(keyword):
    query = urllib.parse.quote(keyword)
    url = NMV + query

    request_movie = urllib.request.Request(url)
    request_movie.add_header("X-Naver-Client-Id", CID)
    request_movie.add_header("X-Naver-Client-Secret", CSC)
    response = urllib.request.urlopen(request_movie)

    rescode = response.getcode()
    if rescode==200:
        result = []
        items = json.loads(response.read().decode("utf-8"))["items"]
        for item in items:
            summary = {
            "title": remove_tags(item["title"]),
            "code": int(item["link"].split("?code=")[1]),
            "image": item["image"],
            "director": item["director"].strip("|"),
            "actor": item["actor"].strip("|"),
            "pubDate": item["pubDate"],
            "naverRating": item["userRating"],
            }
            result.append(summary)
        movie_add(result[0:5])
        return result
    else:
        return print(f"Error Code: {rescode}")


# 네이버영화API 검색 결과 중 상위 5개만 DB에 등록
def movie_add(movies):
    for movie in movies:
        title = movie["title"]
        code = movie["code"]

        url = f"https://movie.naver.com/movie/bi/mi/basic.naver?code={code}"
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        desc = soup.select_one("#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p")

        movie = {
            "code": code,
            "image": movie["image"],
            "title": title,
            "director": movie["director"],
            "actor": movie["actor"],
            "pubDate": movie["pubDate"],
            "naverRating": movie["naverRating"],
            "userRating": "0.00",
            "description": remove_tags(str(desc)),
            "reviews": [],
        }
        find = db.movies.find_one({"code": code})

        cnt = 0
        if find is None:
            db.movies.insert_one(movie)
            cnt += 1
    
    return print(f"{cnt} movies added to DB")


@movie_bp.route("/test", methods=["GET"])
def test():
   a = {
    "name": "kim",
    "birth": 1994,
    "skills": ["node.js", "python3"]
   }   
   return render_template("TESTPAGE.html", a=a)

# 네이버 영화DB 스크랩 -> DB 유지관리용. 웹사이트에는 사용 안될거에요
@movie_bp.route("/scrap", methods=["GET"])
def scrap():
    print("scrap")

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