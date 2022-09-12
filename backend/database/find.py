from bson.objectid import ObjectId
from ..config import Pymongo
from ..util.cookie import token_check
from .tools import *

db = Pymongo.db


def movie_code(code):
    """
    영화 code로 DB 검색
    """
    return db.movies.find_one({"code": code}, {"_id": False})


def review_id(rid):
    """
    리뷰 _id로 DB 검색
    """
    review = db.reviews.find_one({"_id": ObjectId(rid)})
    review["_id"] = str(review["_id"])

    return review

def review_delete_id(rid):
    """
    리뷰 _id로 삭제
    """
    review = db.reviews.find_one({"_id": ObjectId(rid)})
    code = review["code"]
    db.movies.update_one({"code": code}, {"$pull": {"reviews": rid}})
    username = review["username"]
    db.users.update_one({"username": username}, {"$pull": {"reviews": rid}})

    return db.reviews.delete_one({"_id": ObjectId(rid)})


def user_uid(uid):
    """
    uid로 사용자 검색
    """
    return db.users.find_one({"uid": uid}, {"_id": False})


def users_all():
    """
    모든 사용자 검색
    """
    return db.users.find({}, {"_id": False})


def movies_all():
    """
    모든 영화 검색
    """
    return db.movies.find({}, {"_id": False})


def reviews_all():
    """
    모든 리뷰 검색
    """
    return db.reviews.find({})