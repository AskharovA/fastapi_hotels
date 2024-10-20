from pydantic import BaseModel


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(HotelAdd):
    id: int
    images: list[str] | None = []


class HotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None
