from fastapi import Query, APIRouter, Body
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"}
]


@router.get('/')
def get_hotels(
        id_: int | None = Query(None, description="Айди"),
        title: str | None = Query(None, description="Название отеля"),
):
    result = []
    for hotel in hotels:
        if id_ and hotel["id"] != id_:
            continue
        if title and hotel["title"] != title:
            continue
        result.append(hotel)
    return result


@router.post('/')
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi_u_morya",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай у фонтана",
        "name": "dubai_fountain",
    }},
})):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "created"}


@router.put('/{hotel_id}', summary="Обновление данных об отеле")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "updated"}
    else:
        return {"message": "Не найден отель"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Частично обновляются данные об отеле"
)
def update_hotel_partial(hotel_id: int, hotel_data: HotelPATCH):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            return {"status": "updated"}
    else:
        return {"message": "Не найден отель"}


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    hotels[:] = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
