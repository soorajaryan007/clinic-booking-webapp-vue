import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models import ( 
    BookingRequest, 
    EmailVerificationRequest,
    EmailRequest,
    RescheduleRequest,  
)
from app.slot_engine import generate_slots
from app.database import get_connection
from app.cal import (
    send_booking_to_cal,
    get_event_types,
    cancel_booking_on_cal,
    reschedule_booking_on_cal,   # ✅ make sure this exists
)

import httpx
from fastapi import FastAPI, HTTPException


load_dotenv()

app = FastAPI()

CAL_API_KEY = os.getenv("CAL_API_KEY")

CAL_REQUEST_URL = (
    "https://api.cal.com/v2/verified-resources/emails/verification-code/request"
)
CAL_VERIFY_URL = (
    "https://api.cal.com/v2/verified-resources/emails/verification-code/verify"
)

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Root
# -------------------------
@app.get("/")
def root():
    return {"status": "running", "message": "Backend OK"}

# -------------------------
# Event Types
# -------------------------
@app.get("/event-types")
def api_event_types():
    return get_event_types()

# -------------------------
# Availability
# -------------------------
@app.get("/availability")
def availability(event_type_id: int, date: str):
    return generate_slots(event_type_id, date)

# -------------------------
# Time conversion: IST → UTC
# -------------------------
def to_utc(iso_time_str: str) -> str:
    if iso_time_str.endswith("Z"):
        iso_time_str = iso_time_str.replace("Z", "+00:00")

    dt = datetime.fromisoformat(iso_time_str)

    ist_time = dt.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
    utc_time = ist_time.astimezone(ZoneInfo("UTC"))

    return utc_time.isoformat()

# -------------------------
# Booking
# -------------------------
@app.post("/book")
def book(req: BookingRequest):
    start_utc = to_utc(req.start)
    end_utc = to_utc(req.end)

    # 1) Save locally
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO bookings (event_type_id, start, end, name, email) VALUES (?, ?, ?, ?, ?)",
        (req.event_type_id, req.start, req.end, req.name, req.email),
    )
    conn.commit()
    conn.close()

    # 2) Send to Cal.com
    cal_response = send_booking_to_cal(
        req.event_type_id,
        start_utc,
        end_utc,
        req.name,
        req.email,
    )

    if "data" not in cal_response or "uid" not in cal_response["data"]:
        return {
            "status": "error",
            "message": "Booking failed on Cal.com",
            "cal_response": cal_response,
        }

    return {
        "status": "success",
        "booking_uid": cal_response["data"]["uid"],
        "start": req.start,
        "end": req.end,
        "name": req.name,
        "email": req.email,
    }

# -------------------------
# Cancel Booking
# -------------------------
@app.delete("/cancel-booking/{booking_uid}")
def cancel_booking(booking_uid: str):
    cal_response = cancel_booking_on_cal(booking_uid)

    return {
        "status": "success",
        "cancelled": True,
        "cal_response": cal_response,
    }

# =========================================================
# ✅ RESCHEDULE (FIXED WITH PYDANTIC)
# =========================================================



@app.post("/reschedule-booking/{booking_uid}")
def reschedule_booking(
    booking_uid: str,
    payload: RescheduleRequest,
):
    cal_response = reschedule_booking_on_cal(
        booking_uid=booking_uid,
        start=payload.start,
        reason=payload.reschedulingReason,
    )

    return {
        "status": "success",
        "rescheduled": True,
        "cal_response": cal_response,
    }


@app.post("/request-email-verification")
async def request_email_verification(payload: EmailRequest):
    if not CAL_API_KEY:
        raise HTTPException(status_code=500, detail="Cal API key not configured")

    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            CAL_REQUEST_URL,
            headers=headers,
            json={"email": payload.email},
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json(),
        )

    return response.json()


@app.post("/verify-email-code")
async def verify_email_code(payload: EmailVerificationRequest):
    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            CAL_VERIFY_URL,
            headers=headers,
            json=payload.dict(),
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json(),
        )

    return response.json()
