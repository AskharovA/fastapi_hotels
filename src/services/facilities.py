from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService


class FacilityService(BaseService):
    async def create_facility(self, data: FacilityAdd):
        facility = await self.db.facilities.add(data)
        await self.db.commit()
        return facility
