from pydantic import BaseModel, EmailStr

class BookingRequest(BaseModel):
    event_type_id: int
    start: str
    end: str
    name: str
    email: EmailStr
