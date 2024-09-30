from asyncpg import UniqueViolationError
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def add(self, data):
        try:
            await super().add(data)
        except (UniqueViolationError, IntegrityError):
            raise HTTPException(status_code=302, detail="Пользователь уже существует")
