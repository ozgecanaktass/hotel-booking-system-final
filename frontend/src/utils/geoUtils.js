// frontend/src/utils/geoUtils.js
import axios from "axios";

export const geocodeHotel = async (hotelName, city) => {
  try {
    const res = await axios.get("https://us1.locationiq.com/v1/search", {
      params: {
        key: process.env.REACT_APP_LOCATIONIQ_KEY,
        q: `${hotelName}, ${city}`,
        format: "json",
        limit: 1,
      },
    });
    const { lat, lon } = res.data[0];
    return { lat: parseFloat(lat), lon: parseFloat(lon) };
  } catch (err) {
    console.error("Geocoding failed:", err);
    return {
    lat: 41.9028, // Roma'nın merkezi
    lon: 12.4964
    };

  }
};
