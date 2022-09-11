from .aggregation import *
from .find import *
from .tools import *
from ..util.cookie import *


def movie_main(limit=None, skip=0):
    """
    최근 리뷰가 달린 영화
    """
    code = get_codes(reviews_time(), limit)[skip]
    
    return [movie_code(code)]


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
    print("query : ",query)
    print("field : ",field)
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
    print("query : ",query)
    print("field : ",field)
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


CardList = {
    "recent": {
        "get": movie_main,
        "show": 1,
        "max_page": 3,
    }, "now": {
        "get": movies_pubDate,
        "show": 5,
        "max_page": 10,
    }, "trend": {
        "get": movies_rcount,
        "show": 5,
        "max_page": 10,
    }, "trendrev": {
        "get": movies_rcount,
        "show": 6,
        "max_page": 10,
    }, "recentrev": {
        "get": reviews_time,
        "show": 16,
        # "max_page": 10,
    }, "popular": {
        "get": reviews_likes,
        "show": 16,
        # "max_page": 10,
    }, 
}