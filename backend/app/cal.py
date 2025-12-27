import os
import requests
from dotenv import load_dotenv
from app.models import RescheduleRequest
load_dotenv()

# -------------------------------------------------------------------
# Config
# -------------------------------------------------------------------

CAL_API_KEY = os.getenv("CAL_API_KEY")
BASE_URL = "https://api.cal.com/v2"

if not CAL_API_KEY:
    raise RuntimeError("CAL_API_KEY missing in .env")

BASE_HEADERS = {
    "Authorization": f"Bearer {CAL_API_KEY}",
    "Content-Type": "application/json",
}

# -------------------------------------------------------------------
# Event Types
# -------------------------------------------------------------------

def get_event_types():
    """
    Fetch all event types grouped by Cal.com.
    Used by frontend to list selectable events.
    """
    url = f"{BASE_URL}/event-types"
    res = requests.get(url, headers=BASE_HEADERS)
    res.raise_for_status()

    raw = res.json()
    groups = raw.get("data", {}).get("eventTypeGroups", [])

    if not groups:
        return {"status": "success", "events": []}

    events = groups[0].get("eventTypes", [])
    return {"status": "success", "events": events}


def get_event_type_by_id(event_type_id: int):
    """
    Resolve a single event type by ID.
    Used internally to extract slug, username, timezone, hidden flag.
    """
    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "cal-api-version": "2024-06-11",
    }

    res = requests.get(
        f"{BASE_URL}/event-types/{event_type_id}",
        headers=headers,
    )
    res.raise_for_status()

    return res.json()["data"]["eventType"]

# -------------------------------------------------------------------
# Booking
# -------------------------------------------------------------------

def send_booking_to_cal(
    event_type_id: int,
    start: str,
    end: str,
    name: str,
    email: str,
):
    """
    Create a booking in Cal.com.
    """
    url = f"{BASE_URL}/bookings"

    payload = {
        "eventTypeId": event_type_id,
        "start": start,
        "end": end,
        "timeZone": "Asia/Kolkata",
        "language": "en",
        "metadata": {},
        "responses": {
            "name": name,
            "email": email,
        },
    }

    res = requests.post(url, json=payload, headers=BASE_HEADERS)

    try:
        return res.json()
    except Exception:
        return {
            "status": "error",
            "message": "Invalid response from Cal.com",
        }


def cancel_booking_on_cal(booking_uid: str):
    """
    Cancel an existing booking.
    """
    url = f"{BASE_URL}/bookings/{booking_uid}/cancel"

    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "Content-Type": "application/json",
        "cal-api-version": "2024-06-11",
    }

    payload = {
        "cancellationReason": "User requested cancellation",
        "cancelSubsequentBookings": True,
    }

    res = requests.post(url, headers=headers, json=payload, timeout=10)
    res.raise_for_status()

    return res.json()



def reschedule_booking_on_cal(
    booking_uid: str,
    payload: RescheduleRequest,
):
    url = f"{BASE_URL}/bookings/{booking_uid}/reschedule"

    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "Content-Type": "application/json",
        "cal-api-version": "2024-08-13",
    }

    data = {
        "start": payload.start,
    }

    if payload.reschedulingReason:
        data["reschedulingReason"] = payload.reschedulingReason

    if payload.rescheduledBy:
        data["rescheduledBy"] = payload.rescheduledBy

    if payload.emailVerificationCode:
        data["emailVerificationCode"] = payload.emailVerificationCode

    res = requests.post(url, json=data, headers=headers)

    if res.status_code >= 400:
        raise RuntimeError(res.text)

    return res.json()

# -------------------------------------------------------------------
# Canonical Slots (THE CORRECT WAY)
# -------------------------------------------------------------------

def get_slots_canonical(
    *,
    event_type_id: int,
    date: str,
    booking_uid: str | None = None,
):
    """
    Canonical slot resolution.

    Frontend supplies ONLY:
    - eventTypeId
    - date (YYYY-MM-DD)

    Backend resolves:
    - slug
    - username
    - timezone
    - hidden guard
    """

    # 1️⃣ Resolve event
    event = get_event_type_by_id(event_type_id)

    if event.get("hidden"):
        raise RuntimeError("Event type is hidden and cannot expose slots")

    slug = event["slug"]
    user = event["users"][0]
    username = user["username"]
    time_zone = user.get("timeZone") or "UTC"

    # 2️⃣ Build date window
    start = f"{date}T00:00:00.000Z"
    end = f"{date}T23:59:59.999Z"

    # 3️⃣ Query Cal.com slots
    params = {
        "eventTypeSlug": slug,
        "username": username,
        "start": start,
        "end": end,
        "timeZone": time_zone,
        "format": "range",
    }

    if booking_uid:
        params["bookingUidToReschedule"] = booking_uid

    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "cal-api-version": "2024-09-04",
    }

    res = requests.get(f"{BASE_URL}/slots", params=params, headers=headers)
    res.raise_for_status()

    raw = res.json().get("data", {})

    # 4️⃣ Normalize
    slots = []
    for _, day_slots in raw.items():
        for slot in day_slots:
            slots.append({
                "start": slot["start"],
                "end": slot["end"],
            })

    return slots

# -------------------------------------------------------------------
# Schedules (Optional / Debug)
# -------------------------------------------------------------------

def get_schedules_from_cal():
    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "cal-api-version": "2024-06-11",
    }

    res = requests.get(f"{BASE_URL}/schedules", headers=headers)
    res.raise_for_status()

    return res.json()
