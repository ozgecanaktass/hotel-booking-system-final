from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.search_service import search_rooms

search_bp = Blueprint("search", __name__)

@search_bp.route("/search-hotels", methods=["POST"])
@jwt_required(optional=True)
def search_hotels():
    is_logged_in = get_jwt_identity() is not None

    data = request.get_json()
    city = data.get("city")
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    people = data.get("people")

    if not all([city, check_in, check_out, people]):
        return jsonify({"msg": "Missing parameters"}), 400

    try:
        results = search_rooms(city, check_in, check_out, people, is_logged_in)
        return jsonify(results)
    except Exception as e:
        print("SEARCH ERROR:", e)
        return jsonify({"error": "Internal Server Error"}), 500
