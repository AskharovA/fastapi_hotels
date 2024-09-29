from fastapi import Query, APIRouter, Body

from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from sqlalchemy import insert, select, func
from src.repositories.hotels import HotelsRepository

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('/')
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Локация"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
        )


@router.post('/')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "location": "Сочи, ул. моря 1",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай у фонтана",
        "location": "Дубай, ул. шейха 2",
    }},
})):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "created", "data": result}


@router.put('/{hotel_id}', summary="Обновление данных об отеле")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    pass


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Частично обновляются данные об отеле"
)
def update_hotel_partial(hotel_id: int, hotel_data: HotelPATCH):
    pass


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    pass