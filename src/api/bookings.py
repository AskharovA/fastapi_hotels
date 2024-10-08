from fastapi import APIRouter, HTTPException

from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, IncorrectDatesRequestException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def add_booking(db: DBDep, booking_data: BookingAddRequest, user_id: UserIdDep):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")

    try:
        hotel = await db.hotels.get_one(id=room.hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Отеля не существует")
    room_price: int = room.price

    _booking_data = BookingAdd(
        **booking_data.model_dump(), user_id=user_id, price=room_price
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as e:
        raise HTTPException(status_code=409, detail=e.detail)
    except IncorrectDatesRequestException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отеля не существует")
    await db.commit()

    return {"status": "OK", "data": booking}


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_user_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)
