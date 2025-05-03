from flask import Blueprint, request, jsonify, make_response
from decorators import jwt_required

import jwt
import datetime
import bcrypt
import globalaccess

auth_bp = Blueprint('auth_bp', __name__)

blacklist = globalaccess.db.blacklist
users = globalaccess.db.users

####################################### REGISTER ###########################################
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json  # Expecting JSON data

    if not data or not data.get('username') or not data.get('password'):
        return make_response(jsonify({'message': 'Username and password are required'}), 400)

    if users.find_one({'username': data['username']}):
        return make_response(jsonify({'message': 'Username already exists'}), 409)

    hashed_password = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt())

    new_user = {
        'username': data['username'],
        'password': hashed_password,
        'admin': data.get('admin', False)  # Default to False if not provided
    }

    users.insert_one(new_user)
    return make_response(jsonify({'message': 'User registered successfully'}), 201)

####################################### LOGIN ###########################################
@auth_bp.route('/login', methods=['GET'])
def login():
    auth = request.authorization
    if auth:
        user = users.find_one({'username': auth.username})
        if user is not None:
            if bcrypt.checkpw(bytes(auth.password, 'UTF-8'), user['password']):
                token = jwt.encode({
                    'user': auth.username,
                    'admin': user['admin'],
                    'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
                }, globalaccess.SECRET_KEY, algorithm='HS256')
                return make_response(jsonify({'token': token}), 200)
            else:
                return make_response(jsonify({'message': 'Invalid password'}), 401)
        else:
            return make_response(jsonify({'message': 'User not found'}), 404)
    return make_response(jsonify({'message': 'Authentication required'}), 401)


####################################### LOGOUT ###########################################
@auth_bp.route('/logout', methods=['GET'])
@jwt_required
def logout():
    token = request.headers.get('x-access-token')
    if not token:
        return make_response(jsonify({'message': 'Token is missing'}), 400)
    
    blacklist.insert_one({'token': token})
    return make_response(jsonify({'message': 'Logged out'}), 200)

