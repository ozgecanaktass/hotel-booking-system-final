from flask import Blueprint, request, jsonify
from app.services.agent_service import parse_booking_request
from app.services.hotel_service import get_filtered_hotels
from app.services.book_service import book_room_logic
from datetime import datetime

agent_bp = Blueprint("agent", __name__)

chat_context = {
    "last_selected_room": None,
    "last_check_in": None,
    "last_check_out": None,
    "last_people": None
}

@agent_bp.route("/ai/understand", methods=["POST"])
def ai_understand():
    data = request.get_json()
    user_msg = data.get("message")

    if not user_msg:
        return jsonify({"error": "Missing message"}), 400

    try:
        if "book" in user_msg.lower() and "yes" in user_msg.lower():
            room_id = chat_context.get("last_selected_room")
            check_in = chat_context.get("last_check_in")
            check_out = chat_context.get("last_check_out")
            people = chat_context.get("last_people")

            if not all([room_id, check_in, check_out, people]):
                return jsonify({"error": "No previous room found to book."}), 400

            result = book_room_logic(room_id, people, check_in, check_out)
            return jsonify({"msg": "Booking confirmed!", "details": result}), 200

        parsed = parse_booking_request(user_msg)
        if not parsed:
            return jsonify({"error": "AI agent failed to parse user input."}), 200

        city = parsed["city"]
        budget = parsed["budget"]
        check_in = datetime.strptime(parsed.get("check_in", "2025-07-15"), "%Y-%m-%d").date()
        check_out = datetime.strptime(parsed.get("check_out", "2025-07-18"), "%Y-%m-%d").date()
        people = parsed.get("people", 2)
        preferences = parsed.get("preferences", [])
        min_rating = parsed.get("min_rating", 0)

        hotels = get_filtered_hotels(city, budget, check_in, check_out, preferences, min_rating)

        if hotels:
            chat_context["last_selected_room"] = hotels[0]["room_id"]
            chat_context["last_check_in"] = str(check_in)
            chat_context["last_check_out"] = str(check_out)
            chat_context["last_people"] = people

        return jsonify({
            "parsed": parsed,
            "recommendations": hotels
        }), 200

    except Exception as e:
        print("AI ERROR:", e)
        return jsonify({"error": "Internal error"}), 500
