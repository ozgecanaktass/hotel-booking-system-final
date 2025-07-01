from app.services.reservation_queue import pull_all_reservations
from app.services.notification_service import notify_user

def process_reservation_queue():
    print("📦 Pulling reservation queue...")
    reservations = pull_all_reservations()

    if not reservations:
        print("📭 No new reservations to notify.")
        return

    for booking in reservations:
        notify_user(booking)

    print("📬 All reservations processed.\n")
