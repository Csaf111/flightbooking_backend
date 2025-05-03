from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.flight_booking

SECRET_KEY = 'mysecret'

