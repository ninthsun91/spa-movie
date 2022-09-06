import os
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


@app.route("/")
def home():
   return render_template("home.html")


@app.route("/rev")
def review():
   return render_template("review.html")
@app.route("/revcard")
def review_card():
   return render_template("components/review_card.html",movies=[1,2])
@app.route("/postercard")
def poster_card():
   return render_template("components/poster_card.html",movies=[1,2,3,4])



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
   username = request.form["username"]

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


@app.route("/signin")
def components_sign_in():
   return render_template("components/sign_in.html")


@app.route("/signin", methods=["POST"])
def sign_in():
   username = request.form["username"]
   password = request.form["password"]
   if (is_alphs(username) and (2<len(username)<16)) is not True:
      return jsonify({"msg": "아이디 형식은 알파벳,숫자 3~15자 입니다."})
   if (is_alphs(password) and (7<len(password)<16)) is not True:
      return jsonify({"msg": "비밀번호 형식은 알파벳,숫자 8~15자 입니다."})

   password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
   user = db.users.find_one({"username": username, "password": password_hash})
   if user is not None:
      uid = user["uid"]
      payload = {
         "uid": uid,
         "username": username,
         "exp": datetime.utcnow() + timedelta(seconds = 60*60)
      }
      token = jwt.encode(payload, KEY, algorithm="HS256") #.decode("utf-8")   # annotate while running in localhost
      cookie = make_response()
      cookie.set_cookie("logintoken", token)
      return cookie
   else:
      return jsonify({"msg": "아이디, 비밀번호가 틀렸습니다."})


@app.route("/signup")
def components_sign_up():
   return render_template("components/sign_up.html")


@app.route("/signup", methods=["POST"])
def sign_up():
   username = request.form["username"]
   password = request.form["password"]
   if (is_alphs(username) and (2<len(username)<16)) is not True:
      return jsonify({"msg": "아이디 형식은 알파벳,숫자 3~15자 입니다."})
   if (is_alphs(password) and (7<len(password)<16)) is not True:
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

   return redirect(url_for("/sign_in"))


@app.route("/search", methods=["POST"])
def search_title():
   keyword = request.form["keyword"]

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
   if movies.alive:
      result = []
      for movie in movies:
         result.append(movie)
      return jsonify({ result })
   else:
      return redirect("/nsearch", keyword=keyword)


@app.route("/nsearch")
def search_naver():
   keyword = request.args["keyword"]
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
      return f"Error Code: {rescode}"



@app.route("/test", methods=["GET"])
def test():
   return ""


if __name__ == "__main__":
   app.run("0.0.0.0", port=5000, debug=True)


