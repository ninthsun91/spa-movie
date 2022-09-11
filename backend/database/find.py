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


def user_uid():
    payload = token_check()
    if payload is not None:
        uid = payload.get("uid")

        return db.users.find_one({"uid": uid}, {"_id": False})