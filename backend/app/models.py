from pydantic import BaseModel, EmailStr

class BookingRequest(BaseModel):
    event_type_id: int
    start: str
    end: str
    name: str
    email: EmailStr


class EmailRequest(BaseModel):
    email: EmailStr


class EmailVerificationRequest(BaseModel):
    email: EmailStr
    code: str

class RescheduleRequest(BaseModel):
    start: str
    reschedulingReason: str | None = None