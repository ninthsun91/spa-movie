from flask import Blueprint, request, jsonify, make_response
from pymongo import MongoClient

import jwt
import hashlib
import os
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from dotenv import load_dotenv

from ..util.validator import *


load_dotenv()
URL = os.environ.get("MongoDB_URL")
KEY = os.environ.get("HASH_KEY")

client = MongoClient(URL, tls=True, tlsAllowInvalidCertificates=True)
db = client.spamovie

user_bp = Blueprint("user", __name__)


# 로그인
@user_bp.route("/signin", methods=["POST"])
def sign_in():
   username = request.form["username"]
   password = request.form["password"]
   if name_check(username) is not True:
      return jsonify({"msg": "아이디 형식은 알파벳,한글,숫자 3~15자 입니다."})
   if pass_check(password) is not True:
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
      response = make_response({"msg": "login done"})
      response.set_cookie("logintoken", token, timedelta(seconds = 60*60))
      return response
   else:
      return jsonify({"msg": "아이디, 비밀번호가 틀렸습니다."})


# 회원가입
@user_bp.route("/signup", methods=["POST"])
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

   return jsonify({"msg": "success"})


# 프로필 수정
@user_bp.route("/profile", methods=["POST"])
def profile_update():
   token = request.cookies.get("logintoken")
   try:
      payload = jwt.decode(token, KEY, algorithms="HS256")
      uid = payload["uid"]
      username = payload["username"]
      password = request.form["password"]
      if pass_check(password) is not True:
         return jsonify({"msg": "비밀번호 형식은 알파벳,숫자 8~15자 입니다."})
      password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

      profile = {
         "uid": uid,
         "username": username,
         "password": password_hash,
         # etc
      }
      db.users.update_one({"uid": uid}, profile, upsert=True)

      return jsonify({ "msg": "프로필을 수정했습니다." })
   except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
      return jsonify({ "msg": "로그인 세션이 만료되었습니다." })


# 사용자 작성 리뷰 전송
@user_bp.route("/profile/reviews")
def profile_reviews():
   token = request.cookies.get("logintoken")
   try:
      payload = jwt.decode(token, KEY, algorithms="HS256")
      uid = payload["uid"]

      rids = db.users.find_one({"uid": uid}, {"_id": False, "reviews": True})["reviews"]     
      reviews = []
      for rid in rids:
         reviews.append(db.reviews.find_one({"_id": ObjectId(rid)}))
      
      return jsonify({ "reviews": reviews })
   except:
      return jsonify({ "msg": "로그인 세션이 만료되었습니다." })



# 로그인 세션 갱신
def login_renew():
   token = request.cookies.get("logintoken")
   try:
      payload = jwt.decode(token, KEY, algorithms="HS256")
      payload["exp"] = datetime.utcnow() + timedelta(seconds = 60*60)

      token_n = jwt.encode(payload, KEY, algorithm="HS256") #.decode("utf-8")
      response = make_response({"msg": "로그인 세션 갱신"})
      response.set_cookie("logintoken", token_n, timedelta(seconds = 60*60))
      return response
   except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
      return print("로그인 세션이 만료되었습니다.")


# 회원 목록 확인용 임시 도구
@user_bp.route("/userlist")
def userlist():
   users = db.users.find({}, {"_id": False})
   
   result = []
   for user in users:
      result.append(user)
      print(user)
   
   return jsonify({ "users": result })