from flask import session

def initialize_home_session():
    session["list_recent"] = 0
    session["list_now"] = 0
    session["list_trend"] = 0

def initialize_review_session():
    session["review_recent"] = 0
    session["review_trend"] = 0
    session["review_popular"] = 0