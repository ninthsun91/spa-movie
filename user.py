from flask import Blueprint, render_template, request, jsonify, make_response, redirect, url_for
from pymongo import MongoClient

import jwt
import hashlib
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from regex import *


load_dotenv()
URL = os.environ.get("MongoDB_URL")
KEY = os.environ.get("HASH_KEY")

client = MongoClient(URL, tls=True, tlsAllowInvalidCertificates=True)
db = client.spamovie

user_bp = Blueprint("user", __name__)

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
      print("hi1")
      uid = user["uid"]
      payload = {
         "uid": uid,
         "username": username,
         "exp": datetime.utcnow() + timedelta(seconds = 60*60)
      }
      print("hi2")
      print("hi3")
      token = jwt.encode(payload, KEY, algorithm="HS256") #.decode("utf-8")   # annotate while running in localhost
      response = make_response({"msg": "login done"})
      response.set_cookie("logintoken", token)
      print("hi4")
      return response
   else:
      return jsonify({"msg": "아이디, 비밀번호가 틀렸습니다."})

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