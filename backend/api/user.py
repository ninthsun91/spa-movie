from flask import Blueprint, request, jsonify, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
import hashlib
import os

from ..util import *


load_dotenv()
URL = os.environ.get("MongoDB_URL")
KEY = os.environ.get("HASH_KEY")

client = MongoClient(URL, tls=True, tlsAllowInvalidCertificates=True)
db = client.spamovie

user_bp = Blueprint("user", __name__)


# 로그인
@user_bp.route("/signin", methods=["POST"])
def sign_in():
   """
   요청예시: POST, "/signin", data = { username, password }
   반환: logintoken or msg
      logintoken = 로그인 정보를 담은 jwt 토큰
      msg = 실패 메시지 (입력 형식 실패, 인증 실패)
   """
   username = request.form["username"]
   password = request.form["password"]
   if check_name(username) is not True:
      return jsonify({"msg": "아이디 형식은 알파벳,한글,숫자 3~15자 입니다."})
   if check_password(password) is not True:
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
   """
   요청예시: POST, "/signup", data = { username, password }
   반환: msg
      msg = 성공 메시지 / 실패 메시지 (입력 형식 실패)
   """
   username = request.form["username"]
   password = request.form["password"]
   if check_name(username) is not True:
      return jsonify({"msg": "아이디 형식은 알파벳,한글,숫자 3~15자 입니다."})
   if check_password(password) is not True:
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

   return jsonify({"msg": "회원가입을 축하합니다."})


# 프로필 수정
@user_bp.route("/profile", methods=["POST"])
def profile_update():
   """
   요청예시: POST, "/profile", data = { password, email, contact, address, instagram }
   반환: msg
      msg = 성공 메시지 / 실패 메시지 (입력 형식 실패, 로그인 만료)
   """
   token = request.cookies.get("logintoken")
   try:
      payload = jwt.decode(token, KEY, algorithms="HS256")

      uid = payload["uid"]
      username = payload["username"]
      password = request.form["password"]
      if check_password(password) is not True:
         return jsonify({ "msg": "비밀번호 형식은 알파벳,숫자 8~15자 입니다." })
      password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
      email = request.form["email"]
      if check_email(email) is not True:
         return jsonify({ "msg": "잘못된 이메일 형식입니다." })
      contact = request.form["contact"]
      if check_contact(contact) is not True:
         return jsonify({ "msg": "잘못된 전화번호 형식입니다." })
      address = request.form["address"]
      instagram = request.form["instagram"]

      profile = {
         "uid": uid,
         "username": username,
         "password": password_hash,
         "email": email,
         "contact": contact,
         "address": address,
         "instagram": instagram,
         # etc
      }
      db.users.update_one({"uid": uid}, profile, upsert=True)

      return jsonify({ "msg": "프로필을 수정했습니다." })
   except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
      return jsonify({ "msg": "로그인 세션이 만료되었습니다." })


# 사용자 작성 리뷰 전송
@user_bp.route("/profile/reviews")
def profile_reviews():
   """
   요청예시: GET, "/profile/reviews"
      쿼리스트링 불필요
   반환: { reviews: [Array(:dic, length=?)] } or msg
      dic = { _id, code, username, title, comment, userRating, likes, time}
   """
   token = request.cookies.get("logintoken")
   try:
      payload = jwt.decode(token, KEY, algorithms="HS256")
      uid = payload["uid"]

      rids = db.users.find_one({"uid": uid}, {"_id": False, "reviews": True})["reviews"]     
      reviews = []
      for rid in rids:
         review = db.reviews.find_one({"_id": ObjectId(rid)})
         review["_id"] = str(review["_id"])
         reviews.append(review)
      
      return jsonify({ "reviews": reviews })
   except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
      return jsonify({ "msg": "로그인 세션이 만료되었습니다." })


# 회원 목록 확인용 임시 도구
@user_bp.route("/userlist")
def userlist():
   users = db.users.find({}, {"_id": False})
   
   result = []
   for user in users:
      result.append(user)
      print(user)
   
   return jsonify({ "users": result })