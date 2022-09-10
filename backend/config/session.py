from flask import session


"""
세션 쿠키 등록/갱신
페이지네이션은 1
좌우 리스트는 0
"""
def initialize_home_session():
    session["recent"] = 1
    session["now"] = 1
    session["trend"] = 1


def initialize_review_session():
    session["recentrev"] = 1
    session["trendrev"] = 1
    session["popular"] = 1
    session["search"] = 1
    session["keyword"] = ""