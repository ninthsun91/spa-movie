from bson.objectid import ObjectId
from bs4 import BeautifulSoup
import urllib.request
import json
import requests

from ..config import *
from .validator import *

db = Pymongo.db


# MongoDB 영화 code 검색
def movies_code(code):
    return db.movies.find_one({"code": code}, {"_id": False})


# MongoDB 영화 title 검색
def movies_title(keyword, limit=None, skip=0):
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
        }, {"$limit": limit}, {"$skip": skip}
    ]

    # return movies (title matching keyword)
    return list(db.movies.aggregate(pipeline))


# MongoDB 영화 pubDate 검색. 개봉순 정렬
def movies_pubDate(limit=None, skip=0):
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


# MongoDB 영화 검색. reviews 개수 정렬
def movies_rcount(limit=None, skip=0):
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


# MongoDB 리뷰 _id 검색
def reviews_id(rid):
    review = db.reviews.find_one({"_id": ObjectId(rid)})
    review["_id"] = str(review["_id"])

    return review


# MongoDB 리뷰 검색. 최신순 정렬
def reviews_time(limit=None, skip=0):
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


# MongoDB 리뷰 검색. 좋아요순 정렬
def reviews_likes(limit=None, skip=0):
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


# collection 크기
def get_size(collection):
    return db[collection].count_documents({})


# 네이버영화 검색 API
def search_naver(keyword):
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
            "image": item["image"],
            "director": item["director"].strip("|"),
            "actor": item["actor"].strip("|"),
            "pubDate": item["pubDate"],
            "naverRating": item["userRating"],
            }
            result.append(summary)
        movie_add(result[0:5])
        return result
    else:
        return print(f"Error Code: {rescode}")


# 네이버영화API 검색 결과 중 상위 5개만 DB에 등록
def movie_add(movies):
    for movie in movies:
        title = movie["title"]
        code = movie["code"]

        url = f"https://movie.naver.com/movie/bi/mi/basic.naver?code={code}"
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')

        desc = soup.select_one("#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p")
        image = soup.select_one("meta[property='og:image']")["content"].split("?type")[0]
        tag = soup.select_one("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4)")
        pubDate = check_date(remove_tags(str(tag)).strip().replace("\n", ""))
        if pubDate is None:            
            tag = soup.select_one("#content > div.article > div.mv_info_area > div.mv_info > strong").text
            pubDate = "".join(filter(str.isdigit, tag))          

        movie = {
            "code": code,
            "image": image,
            "title": title,
            "director": movie["director"],
            "actor": movie["actor"],
            "pubDate": pubDate,
            "naverRating": movie["naverRating"],
            "userRating": "0.00",
            "description": remove_tags(str(desc)),
            "reviews": [],
        }
        find = db.movies.find_one({"code": code})

        cnt = 0
        if find is None:
            db.movies.insert_one(movie)
            cnt += 1
    
    return print(f"{cnt} movies added to DB")


# 영화 평점(userRating) 계산
def update_rating(code):
    movie = db.movies.find_one({"code": code})

    sum = 0
    r_ids = movie["reviews"]
    for r_id in r_ids:
        review = db.reviews.find_one({"_id": ObjectId(r_id)})
        sum += float(review["userRating"])

    userRating = "{:.2f}".format(sum / len(r_ids))
    db.movies.update_one({"code": code}, {"$set": {"userRating": userRating}})

    return print(f"{code} userRating: {userRating}")