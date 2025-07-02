# 🏨 Hotel Booking System

A full-stack hotel booking platform built for the SE4458 Software Architecture course final project. The system supports hotel room management, user search and booking, comment handling, and an integrated AI agent for natural language hotel interactions.

## 🔗 Deployed URLs

- **Backend API**: [https://hotel-booking-api.onrender.com](https://hotel-booking-system-final.onrender.com)  
---

## 🧩 Features

### 🛠️ Admin Service
- Login with static credentials (`admin` / `1234`)
- Add and update hotel rooms (dates, price, capacity, amenities)
- Protected with JWT authentication

### 🔍 Hotel Search Service
- Search hotels by city, check-in/check-out dates, and number of people
- “Show on map” feature implemented using LocationIQ

### 🛏️ Booking Service
- Book a room from the hotel detail page
- Room capacity is decremented upon booking
- No payment integration (as per requirement)

### 💬 Comments Service
- Users can view hotel-specific comments and service ratings
- Graph shows distribution of ratings per service (cleanliness, location, etc.)
- Comments are stored in **Firestore** (NoSQL DB)

### 🤖 AI Agent
- Natural language interface to search and book hotels
- Connected to the backend via API Gateway
- Prompts the user for preferences (city, dates, rating, amenities) and performs actions accordingly

---

## 🗃️ Technologies Used

| Layer      | Technology |
|------------|------------|
| Backend    | Python (Flask) |
| Frontend   | React (Vite) |
| Database   | PostgreSQL (Render), Firestore (Comments) |
| Auth       | Flask-JWT-Extended |
| AI Agent   | Openai via Gateway |
| Maps       | LocationIQ |
| Deployment | Render |
| CI/CD      | GitHub + Manual Deploy |

---

## 🗂️ Project Structure
```
hotel-booking/
├── app/
│ ├── models/ # SQLAlchemy models (Room, Booking, etc.)
│ ├── routes/ # Flask blueprints for each service
│ ├── services/ # Business logic
│ ├── firebase.py # Firestore setup
│ └── init.py # create_app() Flask factory
├── frontend/ # React app (Vite)
├── seed_rooms.py # Seed script for sample room data
├── requirements.txt
├── Dockerfile
└── README.md

```


## 🔐 Assumptions

- Admin authentication is static and hardcoded
- JWT tokens are stored in localStorage on the frontend
- Room availability is based on date ranges only, not per-night precision
- Firestore is used solely for comments, not bookings
---

## 🗃️ Data Models

### 🛏️ Room Model

| Field          | Type            |
|----------------|-----------------|
| id             | Integer (PK)    |
| hotel_name     | String          |
| city           | String          |
| district       | String          |
| rating         | Float           |
| capacity       | Integer         |
| price          | Float           |
| available_from | Date            |
| available_to   | Date            |
| amenities      | String (CSV)    |

### 📘 Booking Model

| Field           | Type         | Description                      |
|-----------------|--------------|----------------------------------|
| id              | Integer (PK) | Primary key                      |
| room_id         | Integer (FK) | Foreign key to `Room.id`         |
| check_in_date   | Date         | User's check-in date             |
| check_out_date  | Date         | User's check-out date            |
| people          | Integer      | Number of people for the booking |


### Comment (Firestore)
```json
{
  "hotel_name": "Hotel Roma Plaza",
  "user": "Jane Doe",
  "rating": 4.7,
  "services": {
    "cleanliness": 5,
    "location": 4,
    "staff": 5
  },
  "comment": "Very clean and good breakfast!"
}
```
---

- **Demo Video:** [GOOGLE DRIVE](https://drive.google.com/drive/folders/1i3u6wk3YQjN76bIW6hPGDME6h6J2fKva?usp=sharing)
--- 

  👨‍💻 Developed by **Özgecan Aktaş - 21070001019** for SE4458 Final Project- Spring 2025
Instructor: *[Barış Ceyhan]*
