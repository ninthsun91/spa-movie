from flask import session


"""
세션 쿠키 등록/갱신
페이지네이션은 1
좌우 리스트는 0
"""
def initialize_home_session():
    session["home_recent"] = 0
    session["home_now"] = 0
    session["home_trend"] = 0


def initialize_review_session():
    session["review_recent"] = 1
    session["review_trend"] = 0
    session["review_popular"] = 1