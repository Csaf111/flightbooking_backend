import os

from flask import Flask, jsonify
from blueprints.flights.flights import flights_bp
from blueprints.flight_reviews.flight_reviews import reviews_bp
from blueprints.auth.auth import auth_bp
from blueprints.users.users import users_bp
from flask_cors import CORS

app = Flask(__name__)
allowed_origins = [origin.strip() for origin in os.environ.get(
    'CORS_ALLOWED_ORIGINS', 'http://localhost:4200'
).split(',') if origin.strip()]
CORS(app, origins=allowed_origins, supports_credentials=True)

# ✅ Register blueprints
app.register_blueprint(flights_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)


@app.errorhandler(404)
def not_found(_error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(_error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1', port=5001)
