from flask import jsonify, request, abort
from backend.api.auth import bp as auth
from backend.models import UserAccount


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
    new_user = UserAccount.create(email=account_data['email'].lower(),
                                  first=account_data['firstName'],
                                  last=account_data['lastName'],
                                  password=account_data['password']
                           )
    return jsonify('200')

@auth.route('/login', methods=['POST'])
def login():
    account_data = request.json
    print(account_data)
    return jsonify('hi')


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
