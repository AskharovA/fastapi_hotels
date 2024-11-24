from enum import Enum
from datetime import datetime, timezone, timedelta

import jwt
from jwt import DecodeError
from passlib.context import CryptContext

from src.config import settings
from src.exceptions import (
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
    UserNotExistsException,
    IncorrectPasswordException,
    IncorrectTokenException,
)
from src.schemas.users import UserAdd, UserRequestAdd
from src.services.base import BaseService


class TokenType(Enum):
    ACCESS_TOKEN = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    REFRESH_TOKEN = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS)


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register(self, data: UserRequestAdd):
        hashed_password = self.hash_password(password=data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

    async def login_user(self, data: UserRequestAdd):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise UserNotExistsException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token(data={"user_id": user.id})
        refresh_token = self.create_refresh_token(data={"user_id": user.id})
        return {"access_token": access_token, "refresh_token": refresh_token}

    @staticmethod
    def create_token(token_type: TokenType, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + token_type.value
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        return cls.create_token(token_type=TokenType.ACCESS_TOKEN, data=data)

    @classmethod
    def create_refresh_token(cls, data: dict) -> str:
        return cls.create_token(token_type=TokenType.REFRESH_TOKEN, data=data)

    @classmethod
    async def refresh_access_token(cls, refresh_token: str) -> str:
        payload = cls.decode_token(refresh_token)
        user_id: str | None = payload.get("user_id", None)
        new_access_token = cls.create_access_token(data={"user_id": user_id})
        return new_access_token

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except DecodeError:
            raise IncorrectTokenException
