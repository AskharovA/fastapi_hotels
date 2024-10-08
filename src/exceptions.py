from datetime import date
from fastapi import HTTPException


class MyException(Exception):
    detail = "Произошла ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MyException):
    detail = "Объект не найден"


class HotelNotFoundException(MyException):
    detail = "Отель не найден"


class RoomNotFoundException(MyException):
    detail = "Номер не найден"


class AllRoomsAreBookedException(MyException):
    detail = "Не осталось свободных номеров"


class ObjectAlreadyExistsException(MyException):
    detail = "Похожий объект уже существует"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class MyHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(MyHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(MyHTTPException):
    status_code = 404
    detail = "Номер не найден"
