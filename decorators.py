from flask import g, request, jsonify, make_response
import jwt
from functools import wraps
import globalaccess

blacklist = globalaccess.db.blacklist

def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'message': 'Token is missing'}), 401)
        try:
            data = jwt.decode(token, globalaccess.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({'message': 'Token has expired'}), 401)
        except jwt.InvalidTokenError:
            return make_response(jsonify({'message': 'Token is invalid'}), 401)
        
        bl_token = blacklist.find_one({'jti': data.get('jti')})
        if bl_token is not None:
            return make_response(jsonify({'message': 'Token has been revoked'}), 401)

        g.current_user = data['user']
        g.token_claims = data
        
        return func(*args, **kwargs)
    return jwt_required_wrapper
            
def admin_required(func):
    @wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        if g.token_claims.get('admin', False):
            return func(*args, **kwargs)
        else:
            return make_response(jsonify({'message': 'Admin access required'}), 403)
    return admin_required_wrapper
