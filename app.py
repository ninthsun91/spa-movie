import os
from unicodedata import name
import jwt
import hashlib
import json
import urllib.request

from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from datetime import datetime, timedelta
from regex import *
from components import components

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


load_dotenv()
URL = os.environ.get("MongoDB_URL")
KEY = os.environ.get("SECRET_KEY")
NMV = os.environ.get("NMovie_Search")
CID = os.environ.get("Client_ID")
CSC = os.environ.get("Client_Secret")

client = MongoClient(URL, tls=True, tlsAllowInvalidCertificates=True)
db = client.spamovie

app.register_blueprint(components, url_prefix="/components")

@app.route("/")
def home():
   return render_template("home.html")


@app.route("/rev")
def review():
   return render_template("review.html")

@app.route("/movie", methods=["GET"])
def movie_view():
   # code = int(request.args["code"])
   code = 999999
   movie = db.movies.find_one({"code": code}, {"_id": False})

   title = movie["title"]
   director = movie["director"]
   actor = movie["actor"]
   pubDate = movie["pubDate"]
   naverRating = movie["naverRating"]
   userRating = movie["userRating"]
   description = movie["description"]   # optional field
   
   return render_template("movie.html", title=title, director=director, actor=actor, pubDate=pubDate, naverRating=naverRating, userRating=userRating, description=description)


@app.route("/review", methods=["GET"])
def review_view():
   # code = int(request.args["code"])
   code = 999999
   movie = db.movies.find_one({"code": code}, {"_id": False})

   rids = movie["reviews"]
   reviews = []
   for rid in rids:
      reviews.append(db.reviews.find_one({"_id": ObjectId(rid)}))

   return jsonify({ reviews })


@app.route("/review", methods=["POST"])
def review_write():
   code = int(request.form["code"])
   username = request.form["username"]
   title = request.form["title"]
   if title_check(title) is not True:
      return jsonify({"msg": "제목은 특수문자 제외 3~30자입니다."})
   comment = request.form["comment"]
   if (3<=len(comment)<=300) is not True:
      return jsonify({"msg": "3글자 이상 작성해주세요."})
   userRating = request.form["userRating"]
   likes = []
   time = str(datetime.now()).split(".")[0]

   review = {
      "code": code,
      "username": username,
      "title": title,
      "comment": comment,
      "userRating": userRating,
      "likes": likes,
      "time": time,
   }
   db.reviews.insert_one(review)

   return jsonify({"msg": "리뷰를 등록했습니다!"})


@app.route("/like", methods=["POST"])
def review_like():
   id = request.form["id"]
   token = request.cookies.get("logintoken")
   if token is not None:
      try: 
         payload = jwt.decode(token, KEY, algorithms=["HS256"])
         username = payload["username"]

         review = db.reviews.find_one({"_id": ObjectId(id)})
         likes = set(review["likes"])
         if username in likes:
            likes.add(username)
            db.reviews.update_one({"_id": id}, {"$set": {"likes": list(likes)}})
            return jsonify({"msg": "좋아요+1"})
         else:
            likes.remove(username)
            db.reviews.update_one({"_id": id}, {"$set": {"likes": list(likes)}})
            return jsonify({"msg": "좋아요-1"})
      except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
         return ""
   else:
      return ""

@app.route("/signin", methods=["POST"])
def sign_in():
   username = request.form["username"]
   password = request.form["password"]
   if name_check(username) is not True:
      return jsonify({"msg": "아이디 형식은 알파벳,한글,숫자 3~15자 입니다."})
   if pass_check(password) is not True:
      return jsonify({"msg": "비밀번호 형식은 알파벳,숫자 8~15자 입니다."})

   password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
   user = db.users.find_one({"username": username, "password": password_hash})
   print(user)
   if user is not None:
      uid = user["uid"]
      payload = {
         "uid": uid,
         "username": username,
         "exp": datetime.utcnow() + timedelta(seconds = 60*60)
      }
      token = jwt.encode(payload, KEY, algorithm="HS256") #.decode("utf-8")   # annotate while running in localhost
      response = make_response({"msg": "login done"})
      response.set_cookie("logintoken", token)
      return response
   else:
      return jsonify({"msg": "아이디, 비밀번호가 틀렸습니다."})


@app.route("/signup", methods=["POST"])
def sign_up():
   username = request.form["username"]
   password = request.form["password"]
   if name_check(username) is not True:
      return jsonify({"msg": "아이디 형식은 알파벳,한글,숫자 3~15자 입니다."})
   if pass_check(password) is not True:
      return jsonify({"msg": "비밀번호 형식은 알파벳,숫자 8~15자 입니다."})

   cnt = db.users.find_one({}, {"_id": False})
   uid = cnt["cnt"] + 1
   db.users.update_one({}, {"$set": {"cnt": uid}})

   password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
   profile = {
      "uid": uid,
      "username": username,
      "password": password_hash,
      "reviews": []
   }
   db.users.insert_one(profile)
   inserted = db.users.find_one({"username": username}, {"_id": False})
   print(inserted)
   return jsonify({"msg": "sign up success"})


@app.route("/search", methods=["POST"])
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


@app.route("/nsearch")
def search_naver():
   keyword = request.args["keyword"]
   



@app.route("/test", methods=["GET"])
def test():
   a = [1,2,3]
   b = [4,5,6]
   print(a+b)
   return render_template("TESTPAGE.html")


if __name__ == "__main__":
   app.run("0.0.0.0", port=5000, debug=True)


