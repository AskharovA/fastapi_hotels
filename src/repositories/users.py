from asyncpg import UniqueViolationError
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def add(self, data):
        try:
            await super().add(data)
        except (UniqueViolationError, IntegrityError):
            raise HTTPException(status_code=402, detail="Пользователь уже существует")

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model, from_attributes=True)
