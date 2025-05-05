from flask import Blueprint, request, jsonify
from decorators import jwt_required
from flask_cors import cross_origin

import jwt
import datetime
import bcrypt
import globalaccess

auth_bp = Blueprint('auth_bp', __name__)

blacklist = globalaccess.db.blacklist
users = globalaccess.db.users

####################################### REGISTER ###########################################
@auth_bp.route('/register', methods=['POST'])
@cross_origin()
def register():
    data = request.json

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400

    if users.find_one({'username': data['username']}):
        return jsonify({'message': 'Username already exists'}), 409

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    new_user = {
        'username': data['username'],
        'password': hashed_password,
        'admin': data.get('admin', False)
    }

    users.insert_one(new_user)

    # Generate token immediately after signup
    token = jwt.encode({
        'user': new_user['username'],
        'admin': new_user['admin'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, globalaccess.SECRET_KEY, algorithm='HS256')

    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': {'username': new_user['username'], 'admin': new_user['admin']}
    }), 201

####################################### LOGIN ###########################################
@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password required'}), 400

    username = data['username']
    password = data['password']

    user = users.find_one({'username': username})
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    token = jwt.encode({
        'user': username,
        'admin': user.get('admin', False),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, globalaccess.SECRET_KEY, algorithm='HS256')

    return jsonify({
        'token': token,
        'user': {'username': username, 'admin': user.get('admin', False)}
    }), 200

####################################### LOGOUT ###########################################
@auth_bp.route('/logout', methods=['GET'])
@cross_origin()
@jwt_required
def logout():
    token = request.headers.get('x-access-token')
    if not token:
        return jsonify({'message': 'Token is missing'}), 400

    blacklist.insert_one({'token': token})
    return jsonify({'message': 'Logged out successfully'}), 200
