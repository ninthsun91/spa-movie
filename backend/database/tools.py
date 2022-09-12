import requests
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from ordered_set import OrderedSet
from ..config import Pymongo
from ..util.validator import *


db = Pymongo.db


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


def user_fill(user):
    """
    빈 필드 임의 값으로 채워서 전달
    """
    if ("email" not in user) or (user["email"] is ""):
        user["email"] = "email@movie.com"
    if ("contact" not in user) or (user["contact"] is ""):
        user["contact"] = "010-1234-5678"
    if ("address" not in user) or (user["address"] is ""):
        user["address"] = "평양"
    if ("instagram" not in user) or (user["instagram"] is ""):
        user["instagram"] = "instagram.com"

    return user


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


# 네이버 영화DB 스크랩 -> DB 유지관리용
def scrap():
    print("scrap")

    from .aggregation import search_naver

    url = "https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&tg=0&date=20220901"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    body = soup.select_one("#old_content > table > tbody")
    tags = body.select("tr > td.title > div > a")
    for tag in tags:
        title = tag["title"]
        code = int(tag["href"].split("code=")[1])

        naver = search_naver(title)[0]

        url = f"https://movie.naver.com/movie/bi/mi/basic.naver?code={code}"
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        desc = soup.select_one("#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p")
        pubDate = soup.select_one("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4)")

        movie = {
            "code": code,
            "image": naver["image"],
            "title": title,
            "director": naver["director"],
            "actor": naver["actor"],
            "pubDate": remove_tags(str(pubDate)).strip().replace("\n", "")[0:10],
            "naverRating": naver["naverRating"],
            "userRating": "0.00",
            "description": remove_tags(str(desc)),
            "reviews": [],
        }
        find = db.movies.find_one({"code": code})

        if find is None:
            print(f"{title} None")
            db.movies.insert_one(movie)
        else:
            print(f"{title} Exists")

    return ""