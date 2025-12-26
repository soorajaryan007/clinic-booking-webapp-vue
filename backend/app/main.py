import os
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import httpx

from app.models import (
    BookingRequest,
    EmailVerificationRequest,
    EmailRequest,
    RescheduleRequest,
)
from app.database import get_connection
from app.cal import (
    get_event_types,
    send_booking_to_cal,
    cancel_booking_on_cal,
    reschedule_booking_on_cal,
    get_slots_canonical,
    get_schedules_from_cal,
)

load_dotenv()

app = FastAPI()

CAL_API_KEY = os.getenv("CAL_API_KEY")

CAL_REQUEST_URL = "https://api.cal.com/v2/verified-resources/emails/verification-code/request"
CAL_VERIFY_URL = "https://api.cal.com/v2/verified-resources/emails/verification-code/verify"

# -------------------------------------------------
# CORS
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Root
# -------------------------------------------------
@app.get("/")
def root():
    return {"status": "running", "message": "Backend OK"}

# -------------------------------------------------
# Event Types
# -------------------------------------------------
@app.get("/event-types")
def api_event_types():
    return get_event_types()
# -------------------------------------------------
# Canonical Slots
# -------------------------------------------------
from fastapi import HTTPException

@app.get("/slots")
def slots(
    eventTypeId: int = Query(...),
    date: str = Query(..., description="YYYY-MM-DD"),
    bookingUidToReschedule: str | None = Query(None),
):
    try:
        slots = get_slots_canonical(
            event_type_id=eventTypeId,
            date=date,
            booking_uid=bookingUidToReschedule,
        )

        return {
            "status": "success",
            "slots": slots,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# -------------------------------------------------
# Schedules (debug)
# -------------------------------------------------
@app.get("/schedules")
def schedules():
    return get_schedules_from_cal()

# -------------------------------------------------
# Time conversion: IST → UTC
# -------------------------------------------------
def to_utc(iso_time_str: str) -> str:
    if iso_time_str.endswith("Z"):
        iso_time_str = iso_time_str.replace("Z", "+00:00")

    dt = datetime.fromisoformat(iso_time_str)
    ist_time = dt.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
    utc_time = ist_time.astimezone(ZoneInfo("UTC"))

    return utc_time.isoformat()

# -------------------------------------------------
# Booking
# -------------------------------------------------
@app.post("/book")
def book(req: BookingRequest):
    start_utc = to_utc(req.start)
    end_utc = to_utc(req.end)

    # Save locally
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO bookings (event_type_id, start, end, name, email) VALUES (?, ?, ?, ?, ?)",
        (req.event_type_id, req.start, req.end, req.name, req.email),
    )
    conn.commit()
    conn.close()

    # Send to Cal.com
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
# -------------------------------------------------
# Reschedule Booking
# -------------------------------------------------
@app.post("/reschedule-booking/{booking_uid}")
def reschedule_booking(booking_uid: str, payload: RescheduleRequest):
    return {
        "status": "success",
        "rescheduled": True,
        "cal_response": reschedule_booking_on_cal(
            booking_uid=booking_uid,
            start=payload.start,
            reason=payload.reschedulingReason,
        ),
    }


# -------------------------------------------------
# Email Verification
# -------------------------------------------------
@app.post("/request-email-verification")
async def request_email_verification(payload: EmailRequest):
    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.post(CAL_REQUEST_URL, headers=headers, json={"email": payload.email})

    if res.status_code != 200:
        raise HTTPException(res.status_code, res.json())

    return res.json()


@app.post("/verify-email-code")
async def verify_email_code(payload: EmailVerificationRequest):
    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.post(CAL_VERIFY_URL, headers=headers, json=payload.dict())

    if res.status_code != 200:
        raise HTTPException(res.status_code, res.json())

    return res.json()

# -------------------------------------------------
# Cancel Booking
# -------------------------------------------------
@app.delete("/cancel-booking/{booking_uid}")
def cancel_booking(booking_uid: str):
    return {
        "status": "success",
        "cancelled": True,
        "cal_response": cancel_booking_on_cal(booking_uid),
    }

