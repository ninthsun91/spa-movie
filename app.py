from flask import Flask, render_template
from components import components
from movie import movie_bp
from review import review_bp
from user import user_bp


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.register_blueprint(components, url_prefix="/components")
app.register_blueprint(movie_bp, url_prefix="/")
app.register_blueprint(review_bp, url_prefix="/")
app.register_blueprint(user_bp, url_prefix="/")


@app.route("/")
def home():
   return render_template("home.html")
@app.route("/rev")
def review():
   return render_template("review_page.html")

# @app.route("/search", methods=["POST"])
# def search_title():
#    keyword = request.form["keyword"]   
#    result = search_db(keyword) + search_naver(keyword)
#    return jsonify({ result })

# @app.route("/nsearch")
# def search_naver():
#    keyword = request.args["keyword"]
# @app.route("/test", methods=["GET"])
# def test():
#    a = [1,2,3]
#    b = [4,5,6]
#    print(a+b)
#    return render_template("TESTPAGE.html")

if __name__ == "__main__":
   app.run("0.0.0.0", port=5000, debug=True)