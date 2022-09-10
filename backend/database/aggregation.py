import urllib.request
import json
from ..config import Env, Pymongo
from ..util import *
from .tools import *

db = Pymongo.db


def movies_pubDate(limit=None, skip=0):
    """
    영화 최신순(개봉일순) 정렬
    """
    if limit is None:
        limit = get_size("movies")
    pipeline = [
        {
            "$search": {
                "index": "spa_movies",
                "exists": {
                    "path": "pubDate"
                }
            }
        }, {
            "$sort": { "pubDate": -1 , "code": -1}
        }, {
            "$project": {
                "_id": 0,
            }
        }, {"$limit": limit}, {"$skip": skip}
    ]

    # return movies (sort by pubDate)
    return list(db.movies.aggregate(pipeline))


def movies_rcount(limit=None, skip=0):
    """
    영화 리뷰 개수 정렬

    review_count = 리뷰 개수 함께 반환
    """
    if limit is None:
        limit = get_size("movies")
    pipeline = [
        {
            "$project": {
                "_id": 0,
                "code": 1,
                "image": 1,
                "title": 1,
                "director": 1,
                "actor": 1,
                "pubDate": 1,
                "naverRating": 1,
                "userRating": 1,
                "description": 1,
                "reviews": 1,
                "review_count": {"$size": "$reviews"}
            }
        }, {
            "$sort": {
                "review_count": -1,
                "naverRating": -1
            }
        }, {"$limit": limit}, {"$skip": skip}
    ]

    # return movies (sort by reveiw count)
    return list(db.movies.aggregate(pipeline))


def reviews_time(limit=None, skip=0):
    """
    리뷰 최근 업데이트순 정렬
    """
    if limit is None:
        limit = get_size("reviews")
    pipeline = [
        {
            "$sort": {"time": -1}
        }, {"$limit": limit}, {"$skip": skip}
    ]

    reviews = list(db.reviews.aggregate(pipeline))
    for review in reviews:
        review["_id"] = str(review["_id"])

    # return reviews (sort by last updated time)
    return reviews


def reviews_likes(limit=None, skip=0):
    """
    리뷰 좋아요 개수 정렬

    likes = 좋아요 개수가 대신 들어감
    """
    if limit is None:
        limit = get_size("reviews")
    pipeline = [
        {
            "$project": {
                "_id": 1,
                "code": 1,
                "username": 1,
                "title": 1,
                "comment": 1,
                "userRating": 1,
                "likes": {"$size": "$likes"},
                "time": 1,
            }
        }, {
            "$sort": {"likes": -1, "time": -1}
        }, {"$limit": limit}, {"$skip": skip}
    ]

    reviews = list(db.reviews.aggregate(pipeline))
    for review in reviews:
        review["_id"] = str(review["_id"])

    # return reviews (sort by likes count)
    return reviews


def search_db(keyword, limit=None, skip=0):
    """
    keyword로 영화제목 DB 검색
    """
    if limit is None:
        limit = get_size("movies")
    pipeline = [
        {
            "$search": {
                "index": "spa_movies",
                "text": {
                    "query": keyword,
                    "path": "title",
                }
            }
        }, {
            "$project": {
                "_id": 0
            }
        }, {"$limit": limit}, {"$skip": skip}
    ]

    # return movies (title matching keyword)
    return list(db.movies.aggregate(pipeline))



def search_naver(keyword):
    """
    keyword로 영화제목 네이버영화 검색
    """
    query = urllib.parse.quote(keyword)
    url = Env.NMV + query

    request_movie = urllib.request.Request(url)
    request_movie.add_header("X-Naver-Client-Id", Env.CID)
    request_movie.add_header("X-Naver-Client-Secret", Env.CSC)
    response = urllib.request.urlopen(request_movie)

    rescode = response.getcode()
    if rescode==200:
        result = []
        items = json.loads(response.read().decode("utf-8"))["items"]
        for item in items:
            summary = {
            "title": remove_tags(item["title"]),
            "code": int(item["link"].split("?code=")[1]),
            "director": item["director"].strip("|"),
            "actor": item["actor"].strip("|"),
            "pubDate": item["pubDate"],
            "naverRating": item["userRating"],
            }
            result.append(summary)
        movie_add(result[0:10])
        return result
    else:
        return print(f"Error Code: {rescode}")