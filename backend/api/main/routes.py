from flask import jsonify, request
from backend.api.main import bp


@bp.before_request
def before_request():
    print('hi')


@bp.route('/')
def index():
    return jsonify('hi')


@bp.route('/register', methods=['POST'])
def register():
    account_data = request.json

    return jsonify('hi')
