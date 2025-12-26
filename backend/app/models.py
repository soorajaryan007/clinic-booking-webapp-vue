from pydantic import BaseModel, EmailStr

class BookingRequest(BaseModel):
    event_type_id: int
    start: str
    end: str
    name: str
    email: EmailStr


class EmailRequest(BaseModel):
    email: str

class EmailVerificationRequest(BaseModel):
    email: str
    code: str

class RescheduleRequest(BaseModel):
    start: str
    reschedulingReason: str = "User requested reschedule"