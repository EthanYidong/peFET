# TODO: validate input
# TODO: add default fields to JWT (exp, iat, etc.)
# TODO: extract function for JWT token creation

from flask import jsonify, request
import jwt

import bcrypt

from app import app
from models import User


@app.route('/api/account/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = bcrypt.hashpw(
        bytes(data['password'], 'utf-8'), bcrypt.gensalt())

    user = User.get_or_none(email=data['email'])

    if user is not None:
        return jsonify({'errors': ['User already exists']}), 400
    
    User.create(email=data["email"], password=hashed_password)

    token = jwt.encode({
        'sub': data['email'],
    }, app.config['JWT_SECRET'])
    return jsonify({
        'token': token,
    })


@app.route('/api/account/login', methods=['POST'])
def login():
    data = request.get_json()

    try:
        user = User.get(email=data['email'])
    except User.DoesNotExist:
        return jsonify({'errors': ['Incorrect username or password']}), 400

    if bcrypt.checkpw(
        bytes(
            data['password'],
            'utf-8'),
        bytes(
            user.password,
            'utf-8')):
        token = jwt.encode({
            'sub': user.email
        }, app.config['JWT_SECRET'])
        return jsonify({
            'token': token,
        })
    else:
        return jsonify({'errors': ['Incorrect username or password']}), 400


@app.route('/api/account/validate', methods=['POST'])
def validate():
    data = request.get_json()
    try:
        claims = jwt.decode(data['token'], app.config['JWT_SECRET'], ["HS256"])
    except BaseException:
        return jsonify({'errors': ['Invalid token']}), 400
    return jsonify({'email': claims['sub']})
