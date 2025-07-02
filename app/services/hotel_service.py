from app.extensions.redis_client import redis_client
from app.models.room_model import Room
from app import db
import json


def get_hotel_details(hotel_name):
    cache_key = f"hotel:{hotel_name.lower()}"

    cached = redis_client.get(cache_key)
    if cached:
        print("🔁 Cache hit!")
        return json.loads(cached)

    print("❌ Cache miss, pulling from DB...")
    rooms = Room.query.filter_by(hotel_name=hotel_name).all()
    if not rooms:
        return {"error": "Hotel not found"}, 404

    data = [{
        "room_id": room.id,
        "city": room.city,
        "capacity": room.capacity,
        "price": room.price,
        "available_from": str(room.available_from),
        "available_to": str(room.available_to)
    } for room in rooms]

    redis_client.setex(cache_key, 3600, json.dumps(data))

    return data

def get_filtered_hotels(city, budget, check_in, check_out, preferences, min_rating=0):
    rooms = Room.query.filter(
        Room.city.ilike(city),
        Room.price <= budget,
        Room.available_from <= check_in,
        Room.available_to >= check_out,
        Room.rating >= min_rating 
    ).all()

    results = []
    for room in rooms:
        room_amenities = [a.strip().lower() for a in room.amenities.split(",")] if isinstance(room.amenities, str) else []
        if set(preferences).issubset(set(room_amenities)):
            results.append({
                "hotel_name": room.hotel_name,
                "room_id": room.id,
                "price": room.price,
                "rating": room.rating,
                "district": room.district,
                "amenities": room_amenities,
                "available_from": str(room.available_from),
                "available_to": str(room.available_to),
            })

    return results

