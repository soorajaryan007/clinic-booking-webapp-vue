import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// -------- GET APIs --------
export const getEventTypes = () => API.get("/event-types");

export const getAvailability = (params) =>
  API.get("/availability", { params });

// -------- BOOKING APIs --------
export const bookSlotAPI = (payload) =>
  API.post("/book", payload);

export const cancelBookingAPI = (bookingUid) =>
  API.delete(`/cancel-booking/${bookingUid}`);

export const rescheduleBookingAPI = (uid, payload) =>
  API.post(`/reschedule-booking/${uid}`, payload);

// -------- EMAIL VERIFICATION APIs --------
export const requestEmailVerification = (email) =>
  API.post("/request-email-verification", { email });

export const verifyEmailCode = (email, code) =>
  API.post("/verify-email-code", { email, code });

export default API;
