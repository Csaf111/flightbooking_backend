from flask import Blueprint, jsonify
from pymongo import MongoClient

users_bp = Blueprint('users', __name__)
client = MongoClient("mongodb://localhost:27017/")
db = client.flight_booking

@users_bp.route('/users', methods=['GET'])
def get_users():
    users = list(db.users.find({}, {'_id': 0, 'username': 1, 'admin': 1}))
    return jsonify(users)
