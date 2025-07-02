import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ChatbotPage from "./ChatBotPage";
import SearchHotelPage from "./SearchHotelPage";
import AdminPanel from "./AdminPanel";
import AdminLogin from "./AdminLogin";

function App() {
  return (
    <Router>
      <div>
        {/* 🔹 Navigation Bar */}
        <nav style={{
          background: "#f4f4f4",
          padding: "15px",
          display: "flex",
          justifyContent: "center",
          gap: "20px",
          borderBottom: "1px solid #ccc"
        }}>
          <Link to="/chat" style={{ textDecoration: "none" }}>🤖 Chatbot</Link>
          <Link to="/search" style={{ textDecoration: "none" }}>🏨 Hotel Search</Link>
          <Link to="/admin" style={{ textDecoration: "none" }}>🛠️ Admin Panel</Link> {/* ✅ */}
          <Link to="/admin/login">🔐 Admin</Link>

        </nav>

        {/* 🔹 Sayfa içeriği */}
        <Routes>
          <Route path="/chat" element={<ChatbotPage />} />
          <Route path="/search" element={<SearchHotelPage />} />
          <Route path="/admin" element={<AdminPanel />} /> {/* ✅ */}
          <Route path="/admin/login" element={<AdminLogin />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
