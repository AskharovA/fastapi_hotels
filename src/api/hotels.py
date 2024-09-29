from fastapi import Query, APIRouter, Body

from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from sqlalchemy import insert, select

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
    async with (async_session_maker() as session):
        query = select(HotelsOrm)

        if title:
            query = query.filter(HotelsOrm.title.contains(title))
        if location:
            query = query.filter(HotelsOrm.location.contains(location))
        query = (
            query
            .limit(pagination.per_page)
            .offset((pagination.page - 1) * pagination.per_page)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "created"}


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
