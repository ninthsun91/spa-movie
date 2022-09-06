from flask import Blueprint, jsonify, request
from pymongo import MongoClient

import jwt
import os
from bson.objectid import ObjectId
from datetime import datetime
from dotenv import load_dotenv

from regex import *

load_dotenv()
URL = os.environ.get("MongoDB_URL")
KEY = os.environ.get("SECRET_KEY")

client = MongoClient(URL, tls=True, tlsAllowInvalidCertificates=True)
db = client.spamovie

review_bp = Blueprint("review", __name__)


@review_bp.route("/review", methods=["GET"])
def review_view():
   # code = int(request.args["code"])
   code = 999999
   movie = db.movies.find_one({"code": code}, {"_id": False})

   rids = movie["reviews"]
   reviews = []
   for rid in rids:
      reviews.review_bpend(db.reviews.find_one({"_id": ObjectId(rid)}))

   return jsonify({ "reviews": reviews })


@review_bp.route("/review", methods=["POST"])
def review_write():
    code = int(request.form["code"])
    title = request.form["title"]
    if title_check(title) is not True:
        return jsonify({"msg": "제목은 특수문자 제외 3~30자입니다."})
    comment = request.form["comment"]
    if (3<=len(comment)<=300) is not True:
        return jsonify({"msg": "3글자 이상 작성해주세요."})
    userRating = request.form["userRating"]

    token = request.cookies.get("logintoken")
    if token is not None:
        try: 
            payload = jwt.decode(token, KEY, algorithms=["HS256"])
            username = payload["username"]
            review = {
                "code": code,
                "username": username,
                "title": title,
                "comment": comment,
                "userRating": userRating,
                "likes": [],
                "time": str(datetime.now()).split(".")[0],
            }
            id = request.form["id"] if "id" in request.form.keys() else None
            db.reviews.update_one({"_id": ObjectId(id)}, {"$set": review}, upsert=True)

            return jsonify({"msg": "리뷰를 등록했습니다!"})
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return jsonify({"msg": "로그인이 만료되었습니다."})
    else:
        return jsonify({"msg": "로그인을 먼저 해주세요."})   


@review_bp.route("/like", methods=["POST"])
def review_like():
   id = request.form["id"]
   token = request.cookies.get("logintoken")
   if token is not None:
      try: 
         payload = jwt.decode(token, KEY, algorithms=["HS256"])
         uid = payload["uid"]

         review = db.reviews.find_one({"_id": ObjectId(id)})
         likes = set(review["likes"])
         if uid not in likes:
            likes.add(uid)
            db.reviews.update_one({"_id": id}, {"$set": {"likes": list(likes)}})
            return jsonify({"msg": "좋아요+1"})
         else:
            likes.remove(uid)
            db.reviews.update_one({"_id": id}, {"$set": {"likes": list(likes)}})
            return jsonify({"msg": "좋아요-1"})
      except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
         return ""
   else:
      return ""
