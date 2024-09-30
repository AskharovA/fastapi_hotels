from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPATCH
from src.api.hotels import router


@router.get('/{hotel_id}/rooms')
async def get_hotel_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_rooms_by_hotel_id(hotel_id=hotel_id)


@router.get('/rooms/{room_id}')
async def get_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post('/{hotel_id}/rooms')
async def add_room(hotel_id: int, data: RoomAdd = Body(openapi_examples={
    "1": {"summary": "Первая комната", "value": {
        "title": "Стандарт с видом на море",
        "description": "Отсутствует",
        "price": 5000, "quantity": 5},
    }
})):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(data, hotel_id=hotel_id)
        await session.commit()
        return room


@router.put('/rooms/{room_id}')
async def update_room(room_id: int, data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=data, id=room_id)
        await session.commit()

    return {"status": "UPDATED"}


@router.patch('/rooms/{room_id}')
async def update_room_partial(room_id: int, data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=data, exclude_unset=True, id=room_id)
        await session.commit()

    return {"status": "UPDATED"}


@router.delete('/rooms/{room_id}')
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()

    return {"status": "DELETED"}
