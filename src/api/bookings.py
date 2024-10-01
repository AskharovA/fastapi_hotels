from fastapi import APIRouter
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.post('/')
async def add_booking(db: DBDep, booking_data: BookingAddRequest, user_id: UserIdDep):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price

    _booking_data = BookingAdd(**booking_data.model_dump(), user_id=user_id, price=room_price)
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}
