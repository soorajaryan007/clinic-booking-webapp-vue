import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getEventTypes = () => API.get("/event-types");
export const getAvailability = (params) =>
  API.get("/availability", { params });

export const bookSlotAPI = (payload) =>
  API.post("/book", payload);

export const cancelBookingAPI = (uid) =>
  API.post(`/cancel-booking/${uid}`);

export const rescheduleBookingAPI = (uid, payload) =>
  API.post(`/reschedule-booking/${uid}`, payload);

export default API;
