from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.init import redis_manager
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get("/")
@cache(expire=5)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("/")
async def add_facility(
        db: DBDep,
        data: FacilityAdd
):
    facility = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "data": facility}
