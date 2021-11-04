from flask import Blueprint

bp = Blueprint('auth', __name__)

from backend.api.auth import routes
