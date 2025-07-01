from flask import Blueprint, request, jsonify
from app.services.agent_service import parse_booking_request
from app.services.book_service import book_room_logic
from app.services.hotel_service import get_filtered_hotels

gateway_bp = Blueprint("gateway", __name__)

# Basit bir context
chat_context = {}

@gateway_bp.route("/gateway/message", methods=["POST"])
def handle_message():
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"error": "Missing message"}), 400

    try:
        # Rezervasyon niyeti
        if "book it" in message.lower():
            if not all(k in chat_context for k in ["room_id", "people", "check_in", "check_out"]):
                return jsonify({"error": "Incomplete booking context"}), 400

            result = book_room_logic(
                room_id=chat_context["room_id"],
                people=chat_context["people"],
                check_in=chat_context["check_in"],
                check_out=chat_context["check_out"]
            )
            return jsonify({"intent": "confirm_booking", "details": result})

        # Otel arama niyeti
        parsed = parse_booking_request(message)
        if not parsed:
            return jsonify({"error": "Could not parse message"}), 200

        hotels = get_filtered_hotels(
            city=parsed["city"],
            budget=parsed["budget"],
            check_in=parsed["check_in"],
            check_out=parsed["check_out"],
            preferences=parsed.get("preferences", []),
            min_rating=parsed.get("min_rating", 0)
        )

        if hotels:
            chat_context["room_id"] = hotels[0]["room_id"]
            chat_context["check_in"] = parsed["check_in"]
            chat_context["check_out"] = parsed["check_out"]
            chat_context["people"] = parsed.get("people", 2)

        return jsonify({
            "intent": "search_hotel",
            "parsed": parsed,
            "recommendations": hotels
        })

    except Exception as e:
        print("GATEWAY ERROR:", e)
        return jsonify({"error": "Internal error"}), 500
