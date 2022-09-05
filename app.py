import os
import jwt
import hashlib

from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from datetime import datetime, timedelta
from validator import *


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


load_dotenv()
URL = os.environ.get("MongoDB_URL")
KEY = os.environ.get("SECRET_KEY")
CID = os.environ.get("Client_ID")
CSC = os.environ.get("Client_Secret")

client = MongoClient(URL, tls=True, tlsAllowInvalidCertificates=True)
db = client.spamovie


@app.route("/")
def home():
   return render_template("home.html")


@app.route("/movie", methods=["GET"])
def get_movie():
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
def get_review():
   # code = int(request.args["code"])
   code = 999999
   movie = db.movies.find_one({"code": code}, {"_id": False})

   rids = movie["reviews"]
   reviews = []
   for rid in rids:
      reviews.append(db.reviews.find_one({"_id": ObjectId(rid)}))

   return jsonify({ reviews })


@app.route("/review", methods=["POST"])
def post_review():
   code = int(request.form["code"])
   username = request.form["username"]
   comment = request.form["comment"]
   if (3<=len(comment)<=300) is not True:
      return jsonify({"msg": "3글자 이상 작성해주세요."})
   userRating = request.form["userRating"]
   time = str(datetime.now()).split(".")[0]

   review = {
      "code": code,
      "username": username,
      "comment": comment,
      "userRating": userRating,
      "time": time,
   }
   db.reviews.insert_one(review)

   return jsonify({"msg": "리뷰를 등록했습니다!"})


@app.route("/sign_in")
def components_sign_in():
   return render_template("components/sign_in.html")


@app.route("/sign_in", methods=["POST"])
def sign_in():
   SIGNIN_FAIL = jsonify({"result": False, "msg": "아이디, 비밀번호가 틀렸습니다."})
   username = request.form["username"]
   password = request.form["password"]
   if (is_alphs(username) and (2<len(username)<16)) is not True:
      return SIGNIN_FAIL
   if (is_alphs(password) and (7<len(password)<16)) is not True:
      return SIGNIN_FAIL

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
      return jsonify({"result": True, "logintoken": token})
   else:
      return SIGNIN_FAIL


@app.route("/sign_up")
def components_sign_up():
   return render_template("components/sign_up.html")


@app.route("/sign_up", methods=["POST"])
def sign_up():
   SIGNUP_FAIL = jsonify({"msg": "아이디,비밀번호 형식을 확인해주세요."})
   username = request.form["username"]
   password = request.form["password"]
   if (is_alphs(username) and (2<len(username)<16)) is not True:
      return SIGNUP_FAIL
   if (is_alphs(password) and (7<len(password)<16)) is not True:
      return SIGNUP_FAIL

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


if __name__ == "__main__":
   app.run("0.0.0.0", port=5000, debug=True)
