from sqlalchemy import select, func

from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self, title, location, limit, offset):
        query = select(HotelsOrm)

        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
