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
KEY = os.environ.get("HASH_KEY")

client = MongoClient(URL, tls=True, tlsAllowInvalidCertificates=True)
db = client.spamovie

review_bp = Blueprint("review", __name__)


# 리뷰 상세
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


# 리뷰 작성 및 수정
@review_bp.route("/review", methods=["POST"])
def review_write():
    code = int(request.form["code"])
    title = request.form["title"]

    if title_check(title) is not True:
        return jsonify({"msg": "제목은 특수문자 제외 3~30자입니다."})
    comment = request.form["comment"]
    if comment_check(comment) is not True:
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
            up = db.reviews.update_one({"_id": ObjectId(id)}, {"$set": review}, upsert=True)

            db.users.update_one({"username": username}, {"$addToSet": {"reviews": str(up.upserted_id)}})
            db.movies.update_one({"code": code}, {"$addToSet": {"reviews": str(up.upserted_id)}})
            update_rating(code)            

            return jsonify({"msg": "리뷰를 등록했습니다!"})
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return jsonify({"msg": "로그인이 만료되었습니다."})
    else:
        return jsonify({"msg": "로그인을 먼저 해주세요."})   


# 좋아요 수 조회
@review_bp.route("/like")
def count_like():
    id = request.args["id"]

    review = db.reviews.find_one({"_id": ObjectId(id)})
    likes = review["likes"]

    return jsonify({ "likes": len(likes) })


# 좋아요 증감
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


# 영화 평점(userRating) 계산
def update_rating(code):
    movie = db.movies.find_one({"code": code})

    sum = 0
    r_ids = movie["reviews"]
    for r_id in r_ids:
        review = db.reviews.find_one({"_id": ObjectId(r_id)})
        sum += float(review["userRating"])

    userRating = "{:.2f}".format(sum / len(r_ids))
    db.movies.update_one({"code": code}, {"$set": {"userRating": userRating}})

    return print(f"{code} userRating: {userRating}")