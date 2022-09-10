from flask import Blueprint
from .contents import contents_ext
from .modals import modals_ext


components_bp = Blueprint("components", __name__)
components_bp.register_blueprint(contents_ext)
components_bp.register_blueprint(modals_ext)