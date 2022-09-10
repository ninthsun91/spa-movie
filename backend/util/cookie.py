from flask import request, make_response, session
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






def session_page(session_name, query, show):
    """
    : session_name = "recent" | "now" | "trend" | "trendrev" | "recentrev" | "popular" | "search"
    : query = query string
    : show = 한번에 보여주는 개수

    return skip(:int)
    """
    if "page" in query:
        page = int(query["page"])
        session[session_name] = page
    else:
        page = session.get(session_name)
    
    # return skip
    return (page-1) * show



# DEPRECATED
# 카드리스트의 페이지 세션쿠키를 갱신하고 skip값으로 리턴 (좌우 페이지)
# def session_dir(session_name, query, max_page, show=1):
#     """
#     : session_name = "recent" | "now" | "trend" | "trendrev"
#     : query = query string
#     """
#     if "dir" in query:
#         dir = query["dir"]
#         if dir=="right":
#             session[session_name] += 1
#         elif dir=="left":
#             session[session_name] -= 1 
#     if abs(session.get(session_name))==max_page:
#         session[session_name] = 0
#     page = session.get(session_name)

#     # return skip
#     return (page * show) if page>=0 else ((max_page + page) * show)