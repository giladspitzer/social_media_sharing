from flask import jsonify, request, current_app
from backend.api.main import bp
from flask_login import login_required


@bp.route('/protected')
@login_required
def protected():
    return jsonify('hi')


@bp.route('/open')
def register():
    print(request.headers)
    return jsonify('hi')
