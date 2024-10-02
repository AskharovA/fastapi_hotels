from datetime import date

from sqlalchemy import select, func

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            title: str,
            location: str,
            limit: int,
            offset: int
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels = (
            select(HotelsOrm.id)
            .select_from(HotelsOrm)
        )

        if title:
            hotels = hotels.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location:
            hotels = hotels.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))

        hotels = hotels.offset(offset).limit(limit)

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get), RoomsOrm.hotel_id.in_(hotels))
        )

        return await self.get_filtered(self.model.id.in_(hotels_ids_to_get))
