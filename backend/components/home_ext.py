from flask import Blueprint, request, render_template

from ..util import *


home_ext = Blueprint("home_ext", __name__)


@home_ext.route("/postercard")
def poster_list():
    direction = request.args.get("direction")
    query = request.args.get("type")
    field = [ "code", "image", "title", "director", "actor", "pubDate", "naverRating" ]
    
    if query == "search":
        keyword = request.args.get("keyword")
        result = movie_card(query, field, keyword=keyword)
        movies = result["movies"]
        max_page = result["max_page"]    
    else:        
        result = movie_card(query, field)
        movies = result["movies"]
        max_page = result["max_page"]

    return render_template("components/poster_card.html", movies=movies, direction=direction)