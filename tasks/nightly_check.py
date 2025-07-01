from app.models.room_model import Room
from app.services.notification_service import notify_admin
from datetime import date, timedelta
from app import db

def run_nightly_check():
    print("🌙 Running nightly check...")

    one_month_later = date.today() + timedelta(days=30)
    rooms = Room.query.filter(Room.available_to >= date.today()).all()

    for room in rooms:
        # Boş kapasite kontrolü (örnek olarak kapasiteye göre rastgele bir eşik belirlenebilir)
        booked = 0  # Gerçek projede booking tablosundan hesaplanır
        total = room.capacity
        remaining = total - booked

        if total > 0 and (remaining / total) < 0.2:
            notify_admin(room.id, room.hotel_name, remaining, total)

    print("🌙 Nightly check completed.\n")
