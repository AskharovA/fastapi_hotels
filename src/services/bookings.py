from src.exceptions import check_date_to_after_date_from
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.base import BaseService
from src.services.hotels import HotelService
from src.services.rooms import RoomService


class BookingService(BaseService):
    async def add_booking(self, booking_data: BookingAddRequest, user_id: int):
        check_date_to_after_date_from(booking_data.date_from, booking_data.date_to)
        room = await RoomService(self.db).get_room_with_check(room_id=booking_data.room_id)
        hotel = await HotelService(self.db).get_hotel_with_check(hotel_id=room.hotel_id)
        room_price: int = room.price

        _booking_data = BookingAdd(
            **booking_data.model_dump(), user_id=user_id, price=room_price
        )

        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        await self.db.commit()
        return booking

    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_user_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)
