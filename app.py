import os
import jwt
import hashlib

from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


load_dotenv()
URL = os.environ.get("MongoDB_URL")
KEY = os.environ.get("SECRET_KEY")
CID = os.environ.get("Client_ID")
CSC = os.environ.get("Client_Secret")

client = MongoClient(URL, tls=True, tlsAllowInvalidCertificates=True)
db = client.spamovie


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/mov")
def movie():
    return render_template("movie.html")


@app.route("/components/sign_in")
def components_sign_in():
    return render_template("components/sign_in.html")


@app.route("/components/sign_up")
def components_sign_up():
    return render_template("components/sign_up.html")


@app.route("/movie", methods=["GET"])
def get_movie():
    code = request.args["code"]
    movie = db.movies.find_one({"code": code}, {"_id": False})
    return jsonify({"result": "success", "movie": movie})


@app.route("/review", methods=["GET"])
def get_review():
    return "show review"


@app.route("/post", methods=["POST"])
def post_review():
    return "post review"


@app.route("/signin", methods=["POST"])
def sign_in():
    return "sign in"


@app.route("/signout", methods=["GET"])
def sign_out():
    return "sign out"


@app.route("/signup", methods=["POST"])
def sign_up():
    return "sign up"


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
