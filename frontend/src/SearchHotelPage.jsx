// frontend/src/SearchHotelPage.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { geocodeHotel } from './utils/geoUtils';  // ← geocode fonksiyonu burada olacak
import HotelMap from './components/HotelMap';     // ← harita bileşeni burada olacak

function SearchHotelPage() {
  const [city, setCity] = useState('');
  const [checkIn, setCheckIn] = useState('');
  const [checkOut, setCheckOut] = useState('');
  const [people, setPeople] = useState(2);
  const [results, setResults] = useState([]);
  const [hotelsWithCoords, setHotelsWithCoords] = useState([]);
  const [searched, setSearched] = useState(false);

  const handleSearch = async () => {
    try {
      const response = await axios.post("http://localhost:5000/search-hotels", {
        city,
        check_in: checkIn,
        check_out: checkOut,
        people,
      });

      const hotelData = response.data;

      const enriched = await Promise.all(
        hotelData.map(async (hotel) => {
          const coords = await geocodeHotel(hotel.hotel_name, hotel.city);
          return coords ? { ...hotel, ...coords } : null;
        })
      );

      const valid = enriched.filter(Boolean);
      setResults(hotelData);
      setHotelsWithCoords(valid);
      setSearched(true);
    } catch (err) {
      console.error("Hotel search failed", err);
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "auto", paddingTop: "30px" }}>
      <h2>🔍 Hotel Search</h2>
      <input
        type="text"
        placeholder="City"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
      />
      <input
        type="date"
        value={checkIn}
        onChange={(e) => setCheckIn(e.target.value)}
        style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
      />
      <input
        type="date"
        value={checkOut}
        onChange={(e) => setCheckOut(e.target.value)}
        style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
      />
      <input
        type="number"
        min={1}
        value={people}
        onChange={(e) => setPeople(e.target.value)}
        style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
      />
      <button onClick={handleSearch} style={{ padding: "10px", width: "100%" }}>
        Search Hotels
      </button>

      {searched && (
        <div style={{ marginTop: "20px" }}>
          {results.length === 0 ? (
  <p>No hotels found</p>
) : (
  <>
    {results.map((hotel, idx) => (
  <div key={idx} style={{ border: "1px solid #ccc", padding: "10px", marginTop: "10px" }}>
    <h4>{hotel.hotel_name}</h4>
    <p>Price: {hotel.price} ₺</p>
    <p>Capacity: {hotel.capacity}</p>
    <p>Available: {hotel.available_from} to {hotel.available_to}</p>

    {/* 🆕 Rezerve Et Butonu */}
    <button
      onClick={async () => {
        try {
          const token = localStorage.getItem("token");
          const res = await axios.post("http://localhost:5000/book-room", {
            room_id: hotel.id,
            people,
            check_in: checkIn,
            check_out: checkOut,
          }, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          alert("Reservation successful!");
        } catch (err) {
          alert("Reservation failed. Check token or availability.");
          console.error(err);
        }
      }}
    >
      Reserve Room
    </button>
  </div>
))}


{/* 🗺️ Harita bileşeni */}
<HotelMap hotels={hotelsWithCoords} />

  </>
)}

        </div>
      )}
    </div>
  );
}

export default SearchHotelPage;
