from sqlalchemy import select, delete, insert

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper
from src.schemas.facilities import RoomFacility, RoomFacilityAdd


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def edit_room_facilities(self, room_id: int, new_facilities: list[int]) -> None:
        room_facilities_query_result = await self.session.execute(
            select(self.model.facility_id).filter_by(room_id=room_id)
        )
        room_facilities: set[int] = {row[0] for row in room_facilities_query_result}

        to_delete: list[int] = list(room_facilities - set(new_facilities))
        to_add: list[int] = list(set(new_facilities) - room_facilities)

        if to_delete:
            await self.session.execute(
                delete(self.model)
                .where(self.model.facility_id.in_(to_delete))
                .filter_by(room_id=room_id)
            )
        if to_add:
            await self.session.execute(
                insert(self.model).values(
                    [
                        RoomFacilityAdd(room_id=room_id, facility_id=f_id).model_dump()
                        for f_id in to_add
                    ]
                )
            )
