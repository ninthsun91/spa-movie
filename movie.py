from flask import Blueprint, render_template, request, jsonify
from pymongo import MongoClient

import urllib.request
import json
import os
from dotenv import load_dotenv

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


@movie_bp.route("/movie", methods=["GET"])
def movie_view():
   # code = int(request.args["code"])
   code = 999999
   movie = db.movies.find_one({"code": code}, {"_id": False})
   
   return render_template("movie.html", movie=movie)


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
    
    return f"{cnt} movies added to DB"


@movie_bp.route("/test", methods=["GET"])
def test():
   a = {
    "name": "kim",
    "birth": 1994,
    "skills": ["node.js", "python3"]
   }   
   return render_template("TESTPAGE.html", a=a)


@movie_bp.route("/test2")
def test2():
    return ""



# 네이버 영화DB 스크랩 -> DB 유지관리용. 웹사이트에는 사용 안될거에요
# @movie_bp.route("/scrap", methods=["GET"])
def scrap():
    print("scrap")

    url = "https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&tg=0&date=20210625"
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

        movie = {
            "code": code,
            "image": naver["image"],
            "title": title,
            "director": naver["director"],
            "actor": naver["actor"],
            "pubDate": naver["pubDate"],
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