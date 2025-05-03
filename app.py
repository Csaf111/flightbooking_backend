from flask import Flask
from blueprints.flights.flights import flights_bp
from blueprints.flight_reviews.flight_reviews import reviews_bp
from blueprints.auth.auth import auth_bp

app = Flask(__name__)
app.register_blueprint(flights_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
