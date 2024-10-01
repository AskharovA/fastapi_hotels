from pydantic import BaseModel
from datetime import date


class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingAdd(BookingAddRequest):
    user_id: int


class Booking(BookingAdd):
    id: int
    price: int
