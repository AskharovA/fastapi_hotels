from datetime import date

from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomsWithRels
from sqlalchemy.orm import selectinload, joinedload


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomsWithRels.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_room_with_rels(self, hotel_id: int, room_id: int):
        room = await self.session.execute(
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(id=room_id, hotel_id=hotel_id)
        )
        model = room.scalars().one_or_none()
        if model is None:
            return None
        return RoomsWithRels.model_validate(model, from_attributes=True)
