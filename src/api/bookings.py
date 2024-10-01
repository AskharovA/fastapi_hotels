from fastapi import APIRouter, Depends
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, get_current_user_id

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.post('/')
async def add_booking(db: DBDep, booking_data: BookingAddRequest, user_id: int = Depends(get_current_user_id)):
    booking = BookingAdd(**booking_data.model_dump(), user_id=user_id)
    new_booking_data = await db.bookings.add(booking)
    await db.commit()

    return {"status": "OK", "data": new_booking_data}
