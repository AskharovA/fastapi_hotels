from pydantic import BaseModel
from datetime import date


class BookingAddRequest(BaseModel):
    # hotel_id: int
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BookingAddRequest):
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int
