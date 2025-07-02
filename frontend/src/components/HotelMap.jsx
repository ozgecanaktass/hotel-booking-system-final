import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// default icon fix
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png",
});

const HotelMap = ({ hotels }) => {
  console.log("Gelen hoteller:", hotels); // ✅ Artık burada!

  const validHotels = hotels.filter(h => h.lat && h.lon);

  if (validHotels.length === 0) return null;

  const center = [validHotels[0].lat, validHotels[0].lon];

  return (
    <div style={{ height: "400px", marginTop: "20px" }}>
      <MapContainer center={center} zoom={13} style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {validHotels.map((hotel, idx) => (
          <Marker key={idx} position={[hotel.lat, hotel.lon]}>
            <Popup>
              <strong>{hotel.hotel_name}</strong><br />
              Price: {hotel.price} ₺
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};


export default HotelMap;
