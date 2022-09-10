from bson.objectid import ObjectId
from bs4 import BeautifulSoup
from ordered_set import OrderedSet
import urllib.request
import json
import requests

from ..config import *
from .validator import *
from .cookie import *

db = Pymongo.db



"""
single search
"""

def movies_code(code):
    """
    영화 code로 DB 검색
    """
    return db.movies.find_one({"code": code}, {"_id": False})


def reviews_id(rid):
    """
    리뷰 _id로 DB 검색
    """
    review = db.reviews.find_one({"_id": ObjectId(rid)})
    review["_id"] = str(review["_id"])

    return review

def users_uid():
    payload = token_check()
    if payload is not None:
        uid = payload.get("uid")
        
        return db.users.find_one({"uid": uid}, {"_id": False})



"""
search and sort
"""


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


def movie_main(limit=None, skip=0):
    """
    최근 리뷰가 달린 영화
    """
    code = get_codes(reviews_time(), limit)[skip]
    
    return [movies_code(code)]





"""
title search by keword
"""




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


def movie_add(movies):
    """
    네이버영화 검색 결과 DB에 등록
    """
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



"""
process card list
"""


CardList = {
    "recent": {
        "get": movie_main,
        "show": 1,
        "max_page": 3,
    }, "now": {
        "get": movies_pubDate,
        "show": 4,
        "max_page": 10,
    }, "trend": {
        "get": movies_rcount,
        "show": 4,
        "max_page": 10,
    }, "trendrev": {
        "get": movies_rcount,
        "show": 3,
        "max_page": 10,
    }, "recentrev": {
        "get": reviews_time,
        "show": 2,
        # "max_page": 10,
    }, "popular": {
        "get": reviews_likes,
        "show": 2,
        # "max_page": 10,
    }, 
}


def movies_title(field, keyword, page=None):
    """
    : keyword = 검색어
    : page = request.args. 페이지 요청 관련 QS. 없으면 첫페이지 데이터 반환
    """
    search_naver(keyword)

    show = 4
    if page == None or len(page) == 0:
        skip = 0
    elif "page" in page:
        skip = session_page("search", page, show)

    movies = movie_field(search_db(keyword, skip=skip), field)
    max_page = len(movies) / show

    return { "movies": movies, "max_page": max_page }


def movie_card(query: str, field: list, page=None, keyword=None):
    """
    : query = recent | now | trend | trendrev
    : field = 반환을 원하는 데이터 필드
    : page = request.args. 페이지 요청 관련 QS. 없으면 첫페이지 데이터 반환
    : keyword = 검색어. query=search 일때만 입력.

    return { movies, max_page }
    """
    if query == "search":
        session["keyword"] = keyword
        return movies_title(field, keyword, page)

    get = CardList[query]["get"]
    max_page = CardList[query]["max_page"]
    show = CardList[query]["show"]

    # if "dir" in page: 
    #     skip = session_dir(query, page, max_page, show)
    if page == None or len(page) == 0:
        skip = 0
    elif "page" in page:
        skip = session_page(query, page, show)

    movies = get(max_page*show, skip)
    result = movie_field(movies[0:show], field)

    return { "movies": result, "max_page": max_page }


def review_card(query: str, field: list, page=None):
    """
    : query = recentrev | popular
    : field = 반환을 원하는 데이터 필드
    : page = request.args. 페이지 요청 관련 QS. 없으면 첫페이지 데이터 반환

    return { reviews, max_page }
    """
    get = CardList[query]["get"]
    show = CardList[query]["show"]
    reviews = get()
    max_page = len(reviews) / show

    # if "dir" in page: 
    #     skip = session_dir(query, page, max_page, show)
    if page == None or len(page) == 0:
        skip = 0
    elif "page" in page:
        skip = session_page(query, page, show)

    result = review_field(reviews[skip:skip+show], field)

    return { "reviews": result, "max_page": max_page }





"""
others
"""


def get_size(collection):
    """
    collection 크기
    """
    return db[collection].count_documents({})


def get_codes(reviews, limit=100):
    """
    리뷰 리스트에서 영화 code 추출
    """
    codes = OrderedSet()
    for review in reviews:
        codes.add(review["code"])
        if len(codes)==limit:
            break

    return list(codes)


def update_rating(code):
    """
    영화 평점(userRating) 계산
    """
    movie = db.movies.find_one({"code": code})

    sum = 0
    r_ids = movie["reviews"]
    for r_id in r_ids:
        review = db.reviews.find_one({"_id": ObjectId(r_id)})
        sum += float(review["userRating"])

    userRating = "{:.2f}".format(sum / len(r_ids))
    db.movies.update_one({"code": code}, {"$set": {"userRating": userRating}})

    return print(f"{code} userRating: {userRating}")



"""
filter field
"""

def movie_field(movies, field: list):
    """
    영화 필드 정리

    field
        : 출력을 원하는 데이터 field
        : 전체필드 = [ "code", "title", "director", "actor", "pubDate",
                "naverRating", "userRating", "description", "reviews" ]
    """
    keys = set([ "code", "title", "director", "actor", "pubDate",
        "naverRating", "userRating", "description", "reviews" ])
    field = set(field)

    for movie in movies:
        [movie.pop(key) for key in list(keys-field)]    

    return movies


def review_field(reviews, field: list):
    """
    리뷰 필드 정리

    field
        : 출력을 원하는 데이터 field
        : 전체필드 = [ "_id", "code", "username", "title", "comment",
                "userRating", "likes", "time" ]
        
    """
    keys = set([ "_id", "code", "username", "title", "comment",
        "userRating", "likes", "time" ])
    field = set(field)

    for review in reviews:
        [review.pop(key) for key in list(keys-field)]    

    return reviews


def user_field(users, field: list):
    """
    유저 필드 정리

    field
        : 출력을 원하는 데이터 field
        : 전체필드 = [ "uid", "username", "password", "email", "contact",
                "address", "instagram", "reviews" ]
        
    """
    keys = set([ "uid", "username", "password", "email", "contact",
        "address", "instagram", "reviews" ])
    field = set(field)

    for user in users:
        [user.pop(key) for key in list(keys-field)]    

    return users