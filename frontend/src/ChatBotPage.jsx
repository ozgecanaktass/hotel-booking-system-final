// frontend/src/ChatbotPage.jsx

import React, { useState } from 'react';
import axios from 'axios';

function ChatbotPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [hotelComments, setHotelComments] = useState({});

  const handleSend = async (customMessage = null) => {
    const textToSend = customMessage || input.trim();
    if (!textToSend) return;

    const userMessage = { from: "You", text: textToSend };
    setMessages(prev => [...prev, userMessage]);

    try {
      const res = await axios.post("http://localhost:5000/gateway/message", {
        message: textToSend
      });

      const agentMessage = { from: "Agent", text: JSON.stringify(res.data) };
      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      setMessages(prev => [...prev, { from: "Agent", text: "Error occurred." }]);
    }

    if (!customMessage) setInput("");
  };

  const handleSendBooking = (roomId) => {
    handleSend("Yes, book it");
  };

  const handleShowComments = async (roomId) => {
    try {
      const res = await axios.get(`http://localhost:5000/room-comments/${roomId}`);
      setHotelComments(prev => ({
        ...prev,
        [roomId]: res.data
      }));
    } catch (error) {
      console.error("Error fetching comments", error);
    }
  };

  const renderHotelCards = (text) => {
    try {
      const parsed = JSON.parse(text);
      if (parsed.intent === "search_hotel" && parsed.recommendations?.length) {
        return (
          <div>
            <h4>Hotel Recommendations:</h4>
            {parsed.recommendations.map((hotel, idx) => (
              <div key={idx} className="hotel-card" style={{ border: "1px solid #ccc", padding: "10px", marginBottom: "10px" }}>
                <h5>{hotel.hotel_name}</h5>
                <p><strong>Price:</strong> {hotel.price} ₺</p>
                <p><strong>Rating:</strong> {hotel.rating}</p>
                <p><strong>District:</strong> {hotel.district}</p>
                <p><strong>Amenities:</strong> {hotel.amenities.join(", ")}</p>
                <button onClick={() => handleSendBooking(hotel.room_id)}>Reserve Room</button>
                <br />
                <button onClick={() => handleShowComments(hotel.room_id)}>Show Comments</button>
                {hotelComments[hotel.room_id] && (
                  <div style={{ marginTop: "10px", background: "#f9f9f9", padding: "10px" }}>
                    <h6>Comments:</h6>
                    {hotelComments[hotel.room_id].comments.map((comment, i) => (
                      <div key={i}>
                        <p><strong>{comment.service_type}:</strong> {comment.rating}/5 - {comment.comment}</p>
                      </div>
                    ))}
                    <h6>Average Ratings:</h6>
                    {Object.entries(hotelComments[hotel.room_id].service_averages).map(([service, avg], i) => (
                      <p key={i}>{service}: {avg}</p>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        );
      }
    } catch (e) {
      return <p>{text}</p>;
    }
    return <p>{text}</p>;
  };

  const renderMessageContent = (msg) => {
    if (msg.from === "Agent") {
      try {
        const parsed = JSON.parse(msg.text);

        if (parsed.intent === "confirm_booking") {
          return (
            <div style={{ backgroundColor: "#e6ffe6", padding: "10px", border: "1px solid green" }}>
              ✅ {parsed.details?.msg || "No message"}<br />
              Room ID: {parsed.details?.room_id ?? "N/A"}<br />
              Remaining Capacity: {parsed.details?.remaining_capacity ?? "N/A"}
            </div>
          );
        }

        if (parsed.intent === "search_hotel" && parsed.recommendations?.length) {
          return renderHotelCards(msg.text);
        }

        return <pre>{JSON.stringify(parsed, null, 2)}</pre>;

      } catch (e) {
        return <p>{msg.text}</p>;
      }
    }
    return <p>{msg.text}</p>;
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto", paddingTop: "30px" }}>
      <h2>Smart Booking Agent</h2>
      <div style={{ border: "1px solid gray", padding: "10px", minHeight: "400px", marginBottom: "10px" }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ marginBottom: "10px" }}>
            <strong>{msg.from}:</strong>
            {renderMessageContent(msg)}
          </div>
        ))}
      </div>
      <input
        type="text"
        style={{ width: "80%", padding: "10px" }}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={() => handleSend()} style={{ padding: "10px" }}>Send</button>
    </div>
  );
}

export default ChatbotPage;
