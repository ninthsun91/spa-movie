import os
import jwt
import hashlib

from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from datetime import datetime, timedelta


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

@app.route("/rev")
def review():
    return render_template("review.html")



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
      reviews.append(db.reviews.find_one({"_id": ObjectId(rid)}, {"_id": False}))

   return jsonify({ reviews })


@app.route("/review", methods=["POST"])
def post_review():
   code = int(request.form["code"])
   username = request.form["username"]
   comment = request.form["comment"]
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
   username = request.form["username"]
   password = request.form["password"]
   password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

   user = db.users.find_one({"username": username, "password": password_hash})
   if user is not None:
      uid = user["uid"]
      payload = {
         "uid": uid,
         "username": username,
         "exp": datetime.utcnow() + timedelta(seconds = 60*60)
      }
      token = jwt.encode(payload, KEY, algorithm="HS256") #.decode("utf-8")   # annotate while using localhost
      return jsonify({"result": True, "logintoken": token})
   else:
      return jsonify({"result": False, "msg": "아이디, 비밀번호가 틀렸습니다."})


@app.route("/sign_up")
def components_sign_up():
   return render_template("components/sign_up.html")


@app.route("/sign_up", methods=["POST"])
def sign_up():
   username = request.form["username"]
   password = request.form["password"]
   password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

   cnt = db.users.find_one({}, {"_id": False})
   uid = cnt["cnt"] + 1

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
