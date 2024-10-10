from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelAdd, HotelPatch
from src.api.dependencies import PaginationDep
from src.api.dependencies import DBDep
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Локация"),
    date_from: date = Query(examples=["2024-10-01"]),
    date_to: date = Query(examples=["2024-10-15"]),
):
    hotels = await HotelService(db).get_filtered_by_time(
        pagination,
        title,
        location,
        date_from,
        date_to,
    )
    return {"status": "OK", "data": hotels}


@router.get("/{hotel_id}", summary="Получить отель")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "Сочи, ул. моря 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай у фонтана",
                    "location": "Дубай, ул. шейха 2",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Обновление данных об отеле")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "Успешно обновлено"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Частично обновляются данные об отеле",
)
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "Успешно обновлено"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "Успешно удалено"}
