from flask import Blueprint, jsonify, request, render_template
from datetime import datetime

from ..config import Pymongo
from ..database import *
from ..util import *


review_bp = Blueprint("review", __name__)
db = Pymongo.db


# 영화별 리뷰 상세리스트
@review_bp.route("/review", methods=["GET"])
def review_view():
    """
    요청예시: GET, "/review?code=999999"
        code = 영화 code
    반환: { reviews: [Array(:dic, length=?)] }
        dic = { _id, code, username, title, comment, userRating, likes, time }
    """
    code = int(request.args["code"])
    movie = db.movies.find_one({"code": code}, {"_id": False})

    rids = movie["reviews"]
    reviews = []
    for rid in rids:
        reviews.append(review_id(rid))

    return jsonify({ "reviews": reviews })


@review_bp.route("/review", methods=["POST"])
def review_write():
    """
    리뷰 작성/수정

    요청예시: POST, "/review", data = { code(:int), title(str), comment(:str), userRating }
        userRating = 0~10. int로 받아도 되고, 0.00~10.00 소수점 2자리수까지의 str로 받아도됨.
    반환: { msg(:str) }
        msg - 성공/실패 메시지
    """
    code = int(request.form["code"])
    title = request.form["title"]
    if check_title(title) is not True:
        return jsonify({"msg": "제목은 특수문자 제외 3~30자입니다."})
    comment = request.form["comment"]
    if check_comment(comment) is not True:
        return jsonify({"msg": "3글자 이상 작성해주세요."})
    userRating = int(float(request.form["userRating"]))
    payload = token_check()
    if type(payload) is str:
        return jsonify({ "msg": payload })
    username = payload["username"]

    review = {
        "code": code,
        "username": username,
        "title": title,
        "comment": comment,
        "userRating": userRating,
        "likes": [],
        "time": str(datetime.now()).split(".")[0],
    }
    id = request.form["id"] if "id" in request.form.keys() else None
    up = db.reviews.update_one({"_id": ObjectId(id)}, {"$set": review}, upsert=True).upserted_id

    id = up if up is not None else id
    db.users.update_one({"username": username}, {"$addToSet": {"reviews": str(id)}})
    db.movies.update_one({"code": code}, {"$addToSet": {"reviews": str(id)}})
    # update_rating(code)

    return jsonify({"msg": "리뷰를 등록했습니다!"})


# 리뷰 삭제
@review_bp.route("/delete")
def review_delete():
    """
    : GET, "/delete?id=id"
    : id = review _id
    """
    r_id = request.args.get("reviewId")
    review = review_id(r_id)
    payload = token_check()
    if review["username"] == payload["username"]:
        result = review_delete_id(r_id).deleted_count
        if result == 1:
            return jsonify({ "msg": "리뷰를 삭제했습니다!" })
    else:
        return  jsonify({ "msg": "작성자만 삭제할 수 있습니다." })



# 인기 많은 리뷰
@review_bp.route("/popular")        # 리뷰2개, 페이지네이션
def list_popular():
    """
    요청예시
        : GET, "/popular?page=page"
        : page = 1 이상의 자연수
    반환
        : { reviews, max_page }
        : 반환 원하는 필드는 아래 field 리스트에 기입
        : revies 전체필드 = [ "_id", "code", "username", "title", "comment",
                "userRating", "likes", "time" ]
    """
    query = request.args.get("query")
    field = [ "_id", "code", "username", "title", "comment",
        "userRating", "likes", "time" ]
    result = review_card("popular", field, request.args)
    reviews = result["reviews"]
    is_home = request.args["is_home"]

    for review in reviews:
        movie = movie_code(int(review["code"]))
        review["m_title"] = movie["title"]
        review["image"] = movie["image"]

    return render_template("components/review_card.html", 
        reviews=reviews, query=query, is_home=is_home)


# 좋아요 수 조회
@review_bp.route("/like")
def count_like():
    """
    요청예시: GET, "/like?id=id"
        id = 리뷰 id
    반환: likes(:int)
        likes = 좋아요 개수
    """
    id = request.args["id"]

    review = db.reviews.find_one({"_id": ObjectId(id)})
    likes = review["likes"]

    return jsonify({ "likes": len(likes) })


# 좋아요 증감
@review_bp.route("/like", methods=["POST"])
def review_like():
    """
    요청예시: POST, "/like", data = { id }
        id(:str) = 리뷰id
    반환: { msg }
        msg = 좋아요 증감 결과 / 로그인 만료
    """
    id = request.form["id"]
    payload = token_check()
    if type(payload) is str:
      return jsonify({ "msg": payload })
    uid = payload["uid"]

    review = db.reviews.find_one({"_id": ObjectId(id)})
    likes = set(review["likes"])
    if uid not in likes:
        likes.add(uid)
        db.reviews.update_one({"_id": id}, {"$set": {"likes": list(likes)}})
        return jsonify({"msg": "좋아요+1"})
    else:
        likes.remove(uid)
        db.reviews.update_one({"_id": id}, {"$set": {"likes": list(likes)}})
        return jsonify({"msg": "좋아요-1"})
