from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from src.exceptions import AllRoomsAreBookedException
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingDataMapper

from src.repositories.utils import rooms_ids_for_booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking)
            for booking in result.scalars().all()
        ]

    async def add_booking(self, data: BaseModel, hotel_id):
        result = await self.session.execute(
            rooms_ids_for_booking(
                date_from=data.date_from,
                date_to=data.date_to,
                hotel_id=hotel_id,
            )
        )
        rooms_ids: list[int] = result.scalars().all()
        if data.room_id not in rooms_ids:
            raise AllRoomsAreBookedException

        return await self.add(data)
