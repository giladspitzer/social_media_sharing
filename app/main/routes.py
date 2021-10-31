from flask import jsonify
from app.main import bp


@bp.before_request
def before_request():
    print('hi')


@bp.route('/')
def index():
    return jsonify('hi')
