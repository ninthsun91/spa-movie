from flask import session


"""
세션 쿠키 등록/갱신
페이지네이션은 1
좌우 리스트는 0
"""
def initialize_home_session():
    session["recent"] = 0
    session["now"] = 0
    session["trend"] = 0


def initialize_review_session():
    session["recentrev"] = 1
    session["trendrev"] = 0
    session["popular"] = 1