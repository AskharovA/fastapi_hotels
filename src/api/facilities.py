from fastapi import APIRouter
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
# @custom_cache_decorator(expire=10)
@cache(expire=5)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def add_facility(db: DBDep, facility_data: FacilityAdd):
    facility = await FacilityService(db).create_facility(facility_data)
    return {"status": "OK", "data": facility}
