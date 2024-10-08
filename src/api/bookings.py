from fastapi import APIRouter, HTTPException

from src.exceptions import AllRoomsAreBookedException, \
    RoomNotFoundException, AllRoomsAreBookedHTTPException, HotelNotFoundException, HotelNotFoundHTTPException, \
    RoomNotFoundHTTPException
from src.schemas.bookings import BookingAddRequest
from src.api.dependencies import DBDep, UserIdDep
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def add_booking(db: DBDep, booking_data: BookingAddRequest, user_id: UserIdDep):
    try:
        booking = await BookingService(db).add_booking(booking_data, user_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_user_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)
