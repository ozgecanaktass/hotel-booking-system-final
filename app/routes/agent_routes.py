from flask import Blueprint, request, jsonify
from app.services.agent_service import parse_booking_request
from app.services.hotel_service import get_filtered_hotels

from datetime import datetime

agent_bp = Blueprint("agent", __name__)

@agent_bp.route("/ai/understand", methods=["POST"])
def ai_understand():
    data = request.get_json()
    user_msg = data.get("message")

    if not user_msg:
        return jsonify({"error": "Missing message"}), 400

    try:
        parsed = parse_booking_request(user_msg)
        if not parsed:
            return jsonify({"error": "AI agent failed to parse user input."}), 200
        
        city = parsed["city"]
        budget = parsed["budget"]

        check_in = datetime.strptime(parsed.get("check_in", "2025-07-15"), "%Y-%m-%d").date()
        check_out = datetime.strptime(parsed.get("check_out", "2025-07-18"), "%Y-%m-%d").date()

        people = parsed.get("people", 2)
        preferences = parsed.get("preferences", [])

        # 👇 Sadece gerekli 5 parametre veriliyor
        hotels = get_filtered_hotels(city, budget, check_in, check_out, preferences)

        return jsonify({
            "parsed": parsed,
            "recommendations": hotels
        }), 200

    except Exception as e:
        print("AI ERROR:", e)
        return jsonify({"error": "Internal error"}), 500
