from flask import Flask
from flask_cors import CORS  # ✅ Import CORS

from blueprints.flights.flights import flights_bp
from blueprints.flight_reviews.flight_reviews import reviews_bp
from blueprints.auth.auth import auth_bp
from blueprints.users.users import users_bp

app = Flask(__name__)

# ✅ Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

# ✅ Register blueprints
app.register_blueprint(flights_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
