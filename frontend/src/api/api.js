import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// =======================
// GET APIs
// =======================

export const getEventTypes = () =>
  API.get("/event-types");

/**
 * Canonical slot fetch
 * Frontend sends ONLY:
 * - eventTypeId
 * - date (YYYY-MM-DD)
 */
export const getSlots = ({ eventTypeId, date, bookingUidToReschedule }) =>
  API.get("/slots", {
    params: {
      eventTypeId,
      date,
      bookingUidToReschedule,
    },
  });

// =======================
// BOOKING APIs
// =======================

export const bookSlotAPI = (payload) =>
  API.post("/book", payload);

export const cancelBookingAPI = (bookingUid) =>
  API.delete(`/cancel-booking/${bookingUid}`);

export const rescheduleBookingAPI = (
  bookingUid,
  {
    start,
    reschedulingReason,
    rescheduledBy,
    emailVerificationCode,
  }
) =>
  API.post(`/reschedule-booking/${bookingUid}`, {
    start,
    reschedulingReason,
    rescheduledBy,
    emailVerificationCode,
  });


// =======================
// EMAIL VERIFICATION APIs
// =======================

export const requestEmailVerification = (email) =>
  API.post("/request-email-verification", { email });

export const verifyEmailCode = (email, code) =>
  API.post("/verify-email-code", { email, code });

export default API;
