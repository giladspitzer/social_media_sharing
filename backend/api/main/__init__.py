from flask import Blueprint, current_app

bp = Blueprint('main', __name__)

from backend.api.main import routes
