from flask import Blueprint
from .home_ext import home_ext
from .review_ext import review_ext
from .user_ext import user_ext


components_bp = Blueprint("components", __name__)
components_bp.register_blueprint(home_ext)
components_bp.register_blueprint(review_ext)
components_bp.register_blueprint(user_ext)