from typing import Annotated

import jwt
from fastapi import Query, Depends, Request, Response, HTTPException, status
from pydantic import BaseModel

from src.database import async_session_maker
from src.exceptions import IncorrectTokenException, IncorrectTokenHTTPException
from src.services.auth import AuthService
from src.utils.db_manager import DBManager

from src.config import settings


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, le=20)]


PaginationDep = Annotated[PaginationParams, Depends()]


async def renew_access_token_if_needed(request: Request, response: Response) -> str:  # TODO CREATE TWO MODULES
    token = request.cookies.get(settings.ACCESS_TOKEN_KEY)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token")  # TODO
    try:
        AuthService.decode_token(token)
        return token
    except jwt.ExpiredSignatureError:  # TODO CUSTOM EXCEPTIONS
        refresh_token = request.cookies.get(settings.REFRESH_TOKEN_KEY, None)
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token")  # TODO

        try:
            new_access_token = await AuthService.refresh_access_token(refresh_token)
            response.set_cookie(key=settings.ACCESS_TOKEN_KEY, value=new_access_token)
            return new_access_token
        except jwt.InvalidTokenError:  # TODO CUSTOM EXCEPTIONS
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No token")  # TODO


def get_current_user_id(token: str = Depends(renew_access_token_if_needed)) -> int:
    try:
        data = AuthService.decode_token(token)
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
