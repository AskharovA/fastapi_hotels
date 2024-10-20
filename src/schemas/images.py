from pydantic import BaseModel


class HotelImageAdd(BaseModel):
    image_path: str
    hotel_id: int | None = None
    room_id: int | None = None


class HotelImage(HotelImageAdd):
    id: int
