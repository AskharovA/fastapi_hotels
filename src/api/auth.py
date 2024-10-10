from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep
from src.exceptions import (
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserNotExistsException,
    IncorrectPasswordException,
    IncorrectLoginOrPasswordHTTPException,
)
from src.schemas.users import UserRequestAdd

from src.services.auth import AuthService
from src.api.dependencies import DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register(data: UserRequestAdd, db: DBDep):
    try:
        await AuthService(db).register(data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(data)
    except (UserNotExistsException, IncorrectPasswordException):
        raise IncorrectLoginOrPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await db.users.get_one_or_none(id=user_id)


@router.delete("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
