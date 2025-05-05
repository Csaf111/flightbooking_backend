from flask import Blueprint, request, jsonify, make_response
from decorators import jwt_required, admin_required
from bson import ObjectId
import uuid
import datetime
import globalaccess

flights_bp = Blueprint('flights_bp', __name__)

flights = globalaccess.db.flights
bookings = globalaccess.db.bookings

##################################### SEARCH FLIGHTS  #####################################
@flights_bp.route('/flights', methods=['GET'])
def search_flights():
    try:
        departure = request.args.get('departure_location')
        arrival = request.args.get('arrival_location')
        date = request.args.get('date')
        min_price = request.args.get('min_price', type=int)
        max_price = request.args.get('max_price', type=int)
        sort_by = request.args.get('sort_by', default="departure_time")
        sort_order = request.args.get('sort_order', default="asc")

        query = {}
        if departure:
            query["departure_airport"] = departure
        if arrival:
            query["arrival_airport"] = arrival
        if date:
            query["departure_time"] = {"$regex": f"^{date}"}
        if min_price is not None:
            query["price"] = {"$gte": min_price}
        if max_price is not None:
            if "price" in query:
                query["price"]["$lte"] = max_price
            else:
                query["price"] = {"$lte": max_price}

        sort_order_value = 1 if sort_order == "asc" else -1
        flights_list = list(flights.find(query, {"_id": 0}).sort([(sort_by, sort_order_value)]))

        if not flights_list:
            return make_response(jsonify({"error": "No flights found for the given criteria"}), 404)

        return make_response(jsonify(flights_list), 200)

    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)

##################################### GET FLIGHT DETAILS #####################################
@flights_bp.route('/flights/<string:flight_number>', methods=['GET'])
def get_flight_details(flight_number):
    try:
        flight = flights.find_one({'flight_number': flight_number}, {"_id": 0})
        if not flight:
            return make_response(jsonify({"error": "Flight not found"}), 404)
        return make_response(jsonify(flight), 200)
    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)

##################################### BOOK A FLIGHT TICKET #####################################
@flights_bp.route('/bookings', methods=['POST'])
@jwt_required
def book_ticket():
    try:
        data = request.json
        required_fields = ["passenger_name", "passport_number", "email", "phone_number", "flight_number", "seat_class", "contact_details"]
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Missing required fields"}), 400)

        flight_number = data["flight_number"].strip()
        flight = flights.find_one({"flight_number": flight_number})
        if not flight:
            return make_response(jsonify({"error": f"Flight '{flight_number}' not found"}), 404)

        if flight["seats_available"] <= 0:
            return make_response(jsonify({"error": "No seats available"}), 400)

        booking_id = str(uuid.uuid4())
        new_booking = {
            "_id": booking_id,
            "passenger_name": data["passenger_name"],
            "passport_number": data["passport_number"],
            "email": data["email"],
            "phone_number": data["phone_number"],
            "flight_number": flight_number,
            "seat_class": data["seat_class"],
            "contact_details": data["contact_details"],
            "booking_time": datetime.datetime.utcnow()
        }

        bookings.insert_one(new_booking)
        flights.update_one({"flight_number": flight_number}, {"$inc": {"seats_available": -1}})

        return make_response(jsonify({"message": "Booking successful", "booking_id": booking_id, "passenger_details": new_booking}), 201)

    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)

##################################### UPDATE A BOOKING #####################################
@flights_bp.route('/bookings/<string:booking_id>', methods=['PUT'])
@jwt_required
def update_booking(booking_id):
    try:
        data = request.json
        update_fields = {}

        allowed_fields = ["passenger_name", "passport_number", "email", "phone_number", "seat_class", "contact_details"]
        for field in allowed_fields:
            if field in data:
                update_fields[field] = data[field]

        result = bookings.update_one({"_id": booking_id}, {"$set": update_fields})
        if result.matched_count == 0:
            return make_response(jsonify({"error": "Booking not found"}), 404)

        return make_response(jsonify({"message": "Booking updated successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)

##################################### DELETE A BOOKING #####################################
@flights_bp.route('/bookings/<string:booking_id>', methods=['DELETE'])
@jwt_required
def delete_booking(booking_id):
    try:
        result = bookings.delete_one({"_id": booking_id})
        if result.deleted_count == 0:
            return make_response(jsonify({"error": "Booking not found"}), 404)
        return make_response(jsonify({"message": "Booking deleted successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)

##################################### UPDATE FLIGHT STATUS #####################################
@flights_bp.route('/flights/<string:flight_number>/status', methods=['PUT'])
@jwt_required
@admin_required
def update_flight_status(flight_number):
    try:
        data = request.json
        new_status = data.get("status")
        valid_statuses = ["On Time", "Delayed", "Cancelled", "Boarding", "Departed", "Landed"]
        if new_status not in valid_statuses:
            return make_response(jsonify({"error": "Invalid status"}), 400)

        result = flights.update_one({"flight_number": flight_number}, {"$set": {"status": new_status}})
        if result.matched_count == 0:
            return make_response(jsonify({"error": "Flight not found"}), 404)

        return make_response(jsonify({"message": f"Flight status updated to '{new_status}'"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)

##################################### GET ALL BOOKINGS #####################################
@flights_bp.route('/bookings', methods=['GET'])
@jwt_required
def get_all_bookings():
    try:
        bookings_list = list(bookings.find({}))
        for booking in bookings_list:
            booking["_id"] = str(booking["_id"])
        return make_response(jsonify(bookings_list), 200)
    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)

##################################### GET A SPECIFIC BOOKING #####################################
@flights_bp.route('/bookings/<string:booking_id>', methods=['GET'])
@jwt_required
def get_booking(booking_id):
    try:
        booking = bookings.find_one({'_id': booking_id})
        if not booking:
            return make_response(jsonify({"error": "Booking not found"}), 404)
        booking["_id"] = str(booking["_id"])
        return make_response(jsonify(booking), 200)
    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)
