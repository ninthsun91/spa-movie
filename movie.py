from flask import Blueprint, render_template, request, jsonify
from pymongo import MongoClient

import urllib.request
import json
import os
from dotenv import load_dotenv

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
   result = search_db(keyword) + search_naver(keyword)

   return jsonify({ result })


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
            "pubDate": 1
         }
        }
   ]
   movies = db.movies.aggregate(pipeline)
   result = []
   for movie in movies:
      result.append(movie)
   return result


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
            "code": item["link"].split("?code=")[1],
            "director": item["director"].strip("|"),
            "pubDate": item["pubDate"],
         }
         result.append(summary)
      return jsonify({ result })
   else:
      return print(f"Error Code: {rescode}")




@movie_bp.route("/test", methods=["GET"])
def test():
   a = {
    "name": "kim",
    "birth": 1994,
    "skills": ["node.js", "python3"]
   }
   
   return render_template("TESTPAGE.html", a=a)