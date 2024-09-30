from fastapi import APIRouter

from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.repositories.users import UsersRepository

from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/register')
async def register(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}
