from flask import Blueprint, jsonify
from decorators import admin_required, jwt_required
import globalaccess

users_bp = Blueprint('users', __name__)
@users_bp.route('/users', methods=['GET'])
@jwt_required
@admin_required
def get_users():
    users = list(globalaccess.db.users.find({}, {'_id': 0, 'username': 1, 'admin': 1}))
    return jsonify(users)
