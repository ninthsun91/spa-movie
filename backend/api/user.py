from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId

from ..config import *
from ..util import *


user_bp = Blueprint("user", __name__)
db = Pymongo.db


@user_bp.route("/user")
def user_info():
   user = users_uid()

   return jsonify({ "user": user })


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

   user = db.users.find_one({"username": username, "password": password_hash(password)})
   if user is not None:
      return create_token(user)
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

   profile = {
      "uid": uid,
      "username": username,
      "password": password_hash(password),
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
   payload = token_check()
   if type(payload) is str:
      return jsonify({ "msg": payload })

   uid = payload["uid"]
   username = payload["username"]
   password = request.form["password"]
   if check_password(password) is not True:
      return jsonify({ "msg": "비밀번호 형식은 알파벳,숫자 8~15자 입니다." })
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
      "password": password_hash(password),
      "email": email,
      "contact": contact,
      "address": address,
      "instagram": instagram,
      # etc
   }
   db.users.update_one({"uid": uid}, profile, upsert=True)

   return jsonify({ "msg": "프로필을 수정했습니다." })


# 사용자 작성 리뷰 전송
@user_bp.route("/profile/reviews")
def profile_reviews():
   """
   요청예시: GET, "/profile/reviews"
      쿼리스트링 불필요
   반환: { reviews: [Array(:dic, length=?)] } or msg
      dic = { _id, code, username, title, comment, userRating, likes, time}
   """
   payload = token_check()
   if type(payload) is str:
      return jsonify({ "msg": payload })

   uid = payload["uid"]
   rids = db.users.find_one({"uid": uid}, {"_id": False, "reviews": True})["reviews"]
   reviews = []
   for rid in rids:
      review = db.reviews.find_one({"_id": ObjectId(rid)})
      review["_id"] = str(review["_id"])
      reviews.append(review)
   
   return jsonify({ "reviews": reviews })






# 회원 목록 확인용 임시 도구
@user_bp.route("/userlist")
def userlist():
   users = db.users.find({}, {"_id": False})
   
   result = []
   for user in users:
      result.append(user)
      print(user)
   
   return jsonify({ "users": result })