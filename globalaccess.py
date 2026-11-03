import os

from pymongo import MongoClient


MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
SECRET_KEY = os.environ.get("FLIGHT_BOOKING_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "FLIGHT_BOOKING_SECRET_KEY must be set. Generate a long random value and keep it out of source control."
    )

client = MongoClient(MONGO_URI)
db = client.flight_booking

