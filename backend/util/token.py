from flask import request, make_response
from datetime import datetime, timedelta
import jwt
import hashlib

from ..config import Env


def password_hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_token(user):
    payload = {
        "uid": user["uid"],
        "username": user["username"],
        "exp": datetime.utcnow() + timedelta(seconds = 60*60)
    }
    token = jwt.encode(payload, Env.HKY, algorithm="HS256") #.decode("utf-8")   # off in localhost
    response = make_response({ "msg": "로그인 성공"})
    response.set_cookie("logintoken", token, timedelta(seconds = 60*60))
    
    return response

"""
로그인세션 관리
login_check(): 로그인 여부 확인
               페이지/모달 렌더링 할 때
token_check(): 토큰 유효성 확인
               api요청 받을 때
"""
def login_check():
    token = request.cookies.get("logintoken")
    if token is None:
        return True


def token_check():
    token = request.cookies.get("logintoken")
    try:
        payload = jwt.decode(token, Env.HKY, algorithms="HS256")
        return payload
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return "로그인 세션이 만료되었습니다."