from flask import Blueprint, jsonify
from app.services.hotel_service import get_hotel_details

hotel_bp = Blueprint("hotel", __name__)

@hotel_bp.route("/hotel/<string:hotel_name>", methods=["GET"])
def hotel_details(hotel_name):
    result = get_hotel_details(hotel_name)
    return jsonify(result)
from flask import Blueprint, jsonify, request
from app.services.hotel_service import get_hotel_details
from app import db
from app.models.room_model import Room
from datetime import datetime

hotel_bp = Blueprint("hotel", __name__)

# 🔹 Eski endpoint: Belirli otelin detayları
@hotel_bp.route("/hotel/<string:hotel_name>", methods=["GET"])
def hotel_details(hotel_name):
    result = get_hotel_details(hotel_name)
    return jsonify(result)

# 🔹 Yeni endpoint: Tüm otelleri getir
@hotel_bp.route("/rooms", methods=["GET"])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([
        {
            "hotel_name": r.hotel_name,
            "city": r.city,
            "district": r.district,
            "rating": r.rating,
            "capacity": r.capacity,
            "price": r.price,
            "available_from": r.available_from.isoformat(),
            "available_to": r.available_to.isoformat(),
            "amenities": r.amenities
        }
        for r in rooms
    ])

# 🔹 Yeni endpoint: Yeni otel ekle
@hotel_bp.route("/add-room", methods=["POST"])
def add_room():
    data = request.json
    try:
        room = Room(
            hotel_name=data["hotel_name"],
            city=data["city"],
            district=data["district"],
            rating=float(data["rating"]),
            capacity=int(data["capacity"]),
            price=float(data["price"]),
            available_from=datetime.strptime(data["available_from"], "%Y-%m-%d").date(),
            available_to=datetime.strptime(data["available_to"], "%Y-%m-%d").date(),
            amenities=data.get("amenities", "")
        )
        db.session.add(room)
        db.session.commit()
        return jsonify({"message": "Room added"}), 201
    except Exception as e:
        print("ADD ROOM ERROR:", e)
        return jsonify({"error": "Failed to add room"}), 500
