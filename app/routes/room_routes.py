# app/routes/room_routes.py

from flask import Blueprint, request, jsonify
from app.models.room_model import Room
from app import db
from flask_jwt_extended import jwt_required

room_bp = Blueprint("room", __name__)

@room_bp.route("/rooms/<int:room_id>", methods=["PUT"])
@jwt_required()
def update_room(room_id):
    data = request.get_json()
    room = Room.query.get(room_id)

    if not room:
        return jsonify({"msg": "Room not found"}), 404

    room.price = data.get("price", room.price)
    room.capacity = data.get("capacity", room.capacity)
    room.available_from = data.get("available_from", room.available_from)
    room.available_to = data.get("available_to", room.available_to)

    db.session.commit()
    return jsonify({"msg": "Room updated successfully!"})

@room_bp.route("/rooms", methods=["GET"])
@jwt_required()
def get_all_rooms():
    rooms = Room.query.all()
    result = [
        {
            "id": room.id,  
            "hotel_name": room.hotel_name,
            "city": room.city,
            "district": room.district,
            "rating": room.rating,
            "capacity": room.capacity,
            "price": room.price,
            "available_from": room.available_from.isoformat(),
            "available_to": room.available_to.isoformat(),
            "amenities": room.amenities
        }
        for room in rooms
    ]
    return jsonify(result)
