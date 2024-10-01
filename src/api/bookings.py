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


@router.get('/')
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get('/me')
async def get_user_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)
