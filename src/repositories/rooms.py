from datetime import date

from sqlalchemy import select

from src.exceptions import ObjectNotFoundException
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomsDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking
from sqlalchemy.orm import selectinload  # or joinedload ( with unique )


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomsDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.scalars().all()
        ]

    async def get_room_with_rels(self, hotel_id: int, room_id: int):
        room = await self.session.execute(
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(id=room_id, hotel_id=hotel_id)
        )
        model = room.scalars().one_or_none()
        if model is None:
            raise ObjectNotFoundException
        return RoomsDataWithRelsMapper.map_to_domain_entity(model)
