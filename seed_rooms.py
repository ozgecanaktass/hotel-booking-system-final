# seed_rooms.py

from app import create_app, db
from app.models.room_model import Room
from datetime import date

app = create_app()

with app.app_context():
    db.create_all()
    try:
        print("🧹 Deleting old room data...")
        db.session.query(Room).delete()
        db.session.commit()

        print("📦 Inserting sample room data...")

        # Rome
        room1 = Room(
        hotel_name="Madison Hotel",   # ✅ gerçek
        city="Rome",
        district="City Centre",
        rating=4.5,
        capacity=2,
        price=210.0,
        available_from=date(2025, 7, 10),
        available_to=date(2025, 7, 20),
        amenities="Free Wi-Fi, Breakfast, Pool"
    )

        room2 = Room(
            hotel_name="Hotel Sonya",   
            city="Rome",
            district="Monti",
            rating=4.3,
            capacity=2,
            price=250.0,
            available_from=date(2025, 7, 12),
            available_to=date(2025, 7, 25),
            amenities="Free Wi-Fi, Breakfast, Pool"
        )

        room6 = Room(
            hotel_name="Twentyone Hotel",  
            city="Rome",
            district="City Centre",
            rating=4.3,
            capacity=2,
            price=2170.0,
            available_from=date(2025, 7, 10),
            available_to=date(2025, 7, 23),
            amenities="Free Wi-Fi, Breakfast"
        )

        room5 = Room(
            hotel_name="Hotel Virgilio",   
            city="Rome",
            district="Monti",
            rating=4.8,
            capacity=2,
            price=2503.0,
            available_from=date(2025, 7, 17),
            available_to=date(2025, 7, 29),
            amenities="Free Wi-Fi, Breakfast, Pool"
        )

        # Paris
        room3 = Room(
            hotel_name="Paris Luxe Hotel",
            city="Paris",
            district="Champs-Élysées",
            rating=4.6,
            capacity=2,
            price=300.0,
            available_from=date(2025, 7, 12),
            available_to=date(2025, 7, 18),
            amenities="Free Wi-Fi, Breakfast, Pool"
        )

        # Brazil
        room4 = Room(
            hotel_name="Brazilian Paradise",
            city="Brazil",
            district="Copacabana",
            rating=4.2,
            capacity=3,
            price=280.0,
            available_from=date(2025, 7, 10),
            available_to=date(2025, 7, 20),
            amenities="Free Wi-Fi, Pool, Breakfast"
        )

        db.session.add_all([room1, room2, room3, room4])
        db.session.commit()
        print("✅ Sample rooms inserted successfully.")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error occurred while inserting rooms: {e}")
