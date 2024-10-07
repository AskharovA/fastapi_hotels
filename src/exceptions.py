class MyException(Exception):
    detail = "Произошла ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MyException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(MyException):
    detail = "Не осталось свободных номеров"
