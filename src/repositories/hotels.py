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

    # async def get_all(self, title, location, limit, offset):
    #     query = select(HotelsOrm)
    #
    #     if title:
    #         query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
    #     if location:
    #         query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
    #     query = (
    #         query
    #         .limit(limit)
    #         .offset(offset)
    #     )
    #     result = await self.session.execute(query)
    #     return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            # title,
            # location,
            # limit,
            # offset
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        return await self.get_filtered(self.model.id.in_(hotels_ids_to_get))
