# ruff: noqa: E402
from typing import Any, AsyncGenerator
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *a, **kw: lambda f: f).start()

import pytest
import json
from httpx import AsyncClient

from src.api.dependencies import get_db
from src.main import app
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *  # noqa: F403
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"
    assert settings.DB_NAME == "test"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, Any]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool  # noqa


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def add_data(setup_database):
    with open("tests/mock_hotels.json", encoding="utf-8") as hotels_json:
        hotels_data = [HotelAdd.model_validate(hotel) for hotel in json.load(hotels_json)]
    with open("tests/mock_rooms.json", encoding="utf-8") as rooms_json:
        rooms_data = [RoomAdd.model_validate(room) for room in json.load(rooms_json)]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels_data)
        await db_.rooms.add_bulk(rooms_data)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac: AsyncClient, add_data):
    await ac.post("/auth/register", json={"email": "kot@pes.com", "password": "1234"})


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac: AsyncClient):
    await ac.post("/auth/login", json={"email": "kot@pes.com", "password": "1234"})
    assert ac.cookies["BOOKING_ACCESS_TOKEN"]
    assert ac.cookies["BOOKING_REFRESH_TOKEN"]
    yield ac
