from datetime import date
from src.schemas.bookings import BookingAdd, Booking
from src.utils.db_manager import DBManager


async def test_booking_crud(db: DBManager):
    user_id = (await db.users.get_all())[0].id  # type: ignore
    room_id = (await db.rooms.get_all())[0].id  # type: ignore

    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    result = await db.bookings.add(booking_data)
    booking: Booking | None = await db.bookings.get_one_or_none(id=result.id)

    assert booking is not None
    assert booking.id == result.id
    assert booking.user_id == user_id
    assert booking.room_id == room_id
    assert booking.date_from == booking_data.date_from
    assert booking.date_to == booking_data.date_to
    assert booking.price == booking_data.price

    booking_data.price = 5000
    await db.bookings.edit(booking_data, id=booking.id)

    booking: Booking | None = await db.bookings.get_one_or_none(id=booking.id)
    assert booking is not None
    assert booking.price == 5000

    await db.bookings.delete()
    booking: Booking | None = await db.bookings.get_one_or_none(id=result.id)
    assert booking is None
