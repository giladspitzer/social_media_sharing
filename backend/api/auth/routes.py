from flask import jsonify, request, abort, current_app
from backend.api.auth import bp as auth
from backend.models import UserAccount, AccountAuthentication
import jwt
from datetime import datetime, timedelta
from flask_login import current_user, login_required


@auth.route('/register', methods=['POST'])
def register():
    account_data = request.json
    if sorted(['firstName', 'lastName', 'password', 'email']) != sorted(account_data.keys()):
        return "Illegal Payload", 400
    if not UserAccount.check_email_availability(account_data['email'].lower()):
        return "Email already in use", 400
    if len(account_data['password']) < 7:
        print(account_data['password'], len(account_data['password']))
        return "Illegal Password", 400
    UserAccount.create(email=account_data['email'].lower(),
                       first=account_data['firstName'],
                       last=account_data['lastName'],
                       password=account_data['password'],
                       ip=request.remote_addr
                       )
    return jsonify('200')


@auth.route('/login', methods=['POST'])
def login():
    account_data = request.json
    user = UserAccount.get(email=account_data['email'].lower())
    AccountAuthentication.create(user.email if user is not None else None,
                                 account_data['password'],
                                 request.remote_addr,
                                 user.id if user is not None else None)
    if user is None or not user.check_password(account_data['password']):
        abort(403)
    token = jwt.encode({
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=current_app.config.get('TOKEN_TIMEOUT'))},
        current_app.config['SECRET_KEY']).decode()
    refresh_token = jwt.encode({
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=current_app.config.get('REFRESH_TOKEN_TIMEOUT'))},
        current_app.config['SECRET_KEY']).decode()
    return jsonify({"access_token": token, "refresh_token": refresh_token,
                    "access_token_expiry": current_app.config.get('TOKEN_TIMEOUT')})


@auth.route('/set-password', methods=['POST'])
def set_password():
    account_data = request.json
    print(account_data)
    return jsonify('hi')


@auth.route('/check-email', methods=['POST'])
def check_email():
    account_data = request.json
    print(account_data.keys())
    return jsonify('hi')


@auth.route('/refresh', methods=['GET'])
@login_required
def refresh_token():
    token = jwt.encode({
        'sub': current_user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=current_app.config.get('TOKEN_TIMEOUT'))},
        current_app.config['SECRET_KEY']).decode()
    return jsonify({"access_token": token,
                    "access_token_expiry": current_app.config.get('TOKEN_TIMEOUT')})
