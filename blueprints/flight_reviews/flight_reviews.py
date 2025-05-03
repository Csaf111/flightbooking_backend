from flask import Blueprint, request, jsonify, make_response
from decorators import jwt_required, admin_required
from bson import ObjectId
import uuid

import globalaccess

reviews_bp = Blueprint('reviews_bp', __name__)

flights = globalaccess.db.flights

##################################### GET ALL REVIEWS FOR A FLIGHT #####################################
@reviews_bp.route('/flights/<string:f_id>/reviews', methods=['GET'])
def get_review(f_id):
    """Retrieve all reviews for a specific flight"""
    try:
        data_to_return = []
        flight = flights.find_one({'flight_number': f_id}, {'reviews': 1, '_id': 0})

        if not flight or 'reviews' not in flight:
            return make_response(jsonify({"error": "Flight not found or no reviews available"}), 404)

        for review in flight['reviews']:
            review['_id'] = str(review['_id'])
            data_to_return.append(review)

        return make_response(jsonify(data_to_return), 200)

    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)


##################################### GET ALL REVIEWS FROM ALL FLIGHTS #####################################
@reviews_bp.route('/flights/reviews', methods=['GET'])
def get_all_reviews():
    """Retrieve all reviews from all flights"""
    try:
        data_to_return = []

        
        flights_with_reviews = flights.find({"reviews": {"$exists": True, "$ne": []}}, {"flight_number": 1, "reviews": 1, "_id": 0})

        for flight in flights_with_reviews:
            flight_number = flight["flight_number"]
            for review in flight["reviews"]:
                review["_id"] = str(review["_id"])
                review["flight_number"] = flight_number
                data_to_return.append(review)

        if not data_to_return:
            return make_response(jsonify({"error": "No reviews found for any flight"}), 404)

        return make_response(jsonify(data_to_return), 200)

    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)


##################################### ADD A NEW REVIEW #####################################
@reviews_bp.route('/flights/<string:f_id>/reviews', methods=['POST'])
@jwt_required
def add_review(f_id):
    """Add a review for a flight"""
    try:
        data = request.json

        if not data or not data.get('username') or not data.get('comment') or not data.get('star'):
            return make_response(jsonify({"error": "Missing required fields"}), 400)

        try:
            star = int(data.get('star'))
            if star < 1 or star > 5:
                return make_response(jsonify({"error": "Star rating must be between 1 and 5"}), 400)
        except ValueError:
            return make_response(jsonify({"error": "Star rating must be a number"}), 400)

        flight = flights.find_one({'flight_number': f_id})

        if not flight:
            return make_response(jsonify({"error": "Flight not found"}), 404)

        new_review = {
            "_id": str(uuid.uuid4()),
            "username": data['username'],
            "comment": data['comment'],
            "star": star
        }

        flights.update_one({'flight_number': f_id}, {"$push": {"reviews": new_review}})
        return make_response(jsonify({"message": "Review added successfully", "review": new_review}), 201)

    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)


##################################### UPDATE A REVIEW #####################################
@reviews_bp.route('/flights/<string:f_id>/reviews/<string:review_id>', methods=['PUT'])
@jwt_required
def update_review(f_id, review_id):
    """Update a specific review for a flight"""
    try:
        data = request.json
        flight = flights.find_one({'flight_number': f_id})

        if not flight:
            return make_response(jsonify({"error": "Flight not found"}), 404)

        updated_reviews = []
        review_found = False

        for review in flight["reviews"]:
            if str(review["_id"]) == review_id:
                review["username"] = data.get("username", review["username"])
                review["comment"] = data.get("comment", review["comment"])
                review["star"] = data.get("star", review["star"])
                review_found = True
            updated_reviews.append(review)

        if not review_found:
            return make_response(jsonify({"error": "Review not found"}), 404)

        flights.update_one({'flight_number': f_id}, {"$set": {"reviews": updated_reviews}})
        return make_response(jsonify({"message": "Review updated successfully"}), 200)

    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)


##################################### DELETE A REVIEW  #####################################
@reviews_bp.route('/flights/<string:f_id>/reviews/<string:review_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_review(f_id, review_id):
    """Admin can delete a specific review from a flight"""
    try:
        flight = flights.find_one({'flight_number': f_id})

        if not flight:
            return make_response(jsonify({"error": "Flight not found"}), 404)

        updated_reviews = [review for review in flight["reviews"] if str(review["_id"]) != review_id]

        if len(updated_reviews) == len(flight["reviews"]):
            return make_response(jsonify({"error": "Review not found"}), 404)

        flights.update_one({'flight_number': f_id}, {"$set": {"reviews": updated_reviews}})
        return make_response(jsonify({"message": "Review deleted successfully"}), 200)

    except Exception as e:
        return make_response(jsonify({"error": "Internal Server Error", "details": str(e)}), 500)
