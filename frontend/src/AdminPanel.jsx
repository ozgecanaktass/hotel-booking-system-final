import React, { useState, useEffect } from "react";
import axios from "axios";

function AdminPanel() {
  const token = localStorage.getItem("token"); // ✅ JWT token alınır

  const [formData, setFormData] = useState({
    hotel_name: "",
    city: "",
    district: "",
    rating: 4,
    capacity: 1,
    price: 100,
    available_from: "",
    available_to: "",
    amenities: "",
  });

  const [updateData, setUpdateData] = useState({
    roomId: "",
    price: "",
    capacity: "",
    available_from: "",
    available_to: "",
  });

  const [hotels, setHotels] = useState([]);
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleUpdateChange = (e) => {
    setUpdateData({ ...updateData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      await axios.post("http://localhost:5000/admin/add-room", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      alert("Hotel added!");
      fetchHotels();
    } catch (err) {
      console.error("Add room failed", err);
    }
  };

  const handleUpdateRoom = async () => {
    try {
      const { roomId, ...payload } = updateData;
      const res = await axios.put(`http://localhost:5000/rooms/${roomId}`, payload, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMessage(res.data.msg);
      fetchHotels();
    } catch (err) {
      console.error("Update failed", err);
      setMessage("Update failed");
    }
  };

  const fetchHotels = async () => {
    try {
      const res = await axios.get("http://localhost:5000/rooms", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setHotels(res.data);
    } catch (err) {
      console.error("Fetch hotels failed", err);
    }
  };

  useEffect(() => {
    fetchHotels();
  }, [fetchHotels]);

  return (
    <div style={{ maxWidth: "800px", margin: "auto", paddingTop: "30px" }}>
      <h2>🛠️ Admin Panel</h2>

      <h4>Add New Hotel</h4>
      <input name="hotel_name" placeholder="Hotel Name" onChange={handleChange} />
      <input name="city" placeholder="City" onChange={handleChange} />
      <input name="district" placeholder="District" onChange={handleChange} />
      <input name="rating" type="number" step="0.1" placeholder="Rating" onChange={handleChange} />
      <input name="capacity" type="number" placeholder="Capacity" onChange={handleChange} />
      <input name="price" type="number" placeholder="Price" onChange={handleChange} />
      <input name="available_from" type="date" onChange={handleChange} />
      <input name="available_to" type="date" onChange={handleChange} />
      <input name="amenities" placeholder="Amenities (comma separated)" onChange={handleChange} />
      <button onClick={handleSubmit}>Add Hotel</button>

      <hr style={{ margin: "30px 0" }} />

      <h4>Update Existing Room</h4>
      <input name="roomId" type="number" placeholder="Room ID" onChange={handleUpdateChange} />
      <input name="price" type="number" placeholder="New Price" onChange={handleUpdateChange} />
      <input name="capacity" type="number" placeholder="New Capacity" onChange={handleUpdateChange} />
      <input name="available_from" type="date" onChange={handleUpdateChange} />
      <input name="available_to" type="date" onChange={handleUpdateChange} />
      <button onClick={handleUpdateRoom}>Update Room</button>
      {message && <p style={{ marginTop: "10px" }}>{message}</p>}

      <h4 style={{ marginTop: "30px" }}>Existing Rooms</h4>
      {hotels.map((h, i) => (
        <div key={i} style={{ border: "1px solid #ccc", padding: "10px", marginTop: "10px" }}>
          <strong>ID {h.id}:</strong> {h.hotel_name} - {h.city} ({h.capacity}p) — {h.price} ₺
        </div>
      ))}
    </div>
  );
}

export default AdminPanel;
