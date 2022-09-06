from flask import Flask, render_template

from movie import movie_bp
from review import review_bp
from user import user_bp


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.register_blueprint(movie_bp, url_prefix="/")
app.register_blueprint(review_bp, url_prefix="/")
app.register_blueprint(user_bp, url_prefix="/")


@app.route("/")
def home():
   return render_template("home.html")


@app.route("/rev")
def review():
   return render_template("review.html")
@app.route("/revcard")
def review_card():
   return render_template("components/review_card.html",movies=[1,2])
@app.route("/postercard")
def poster_card():
   return render_template("components/poster_card.html",movies=[1,2,3,4])






   






if __name__ == "__main__":
   app.run("0.0.0.0", port=5000, debug=True)


