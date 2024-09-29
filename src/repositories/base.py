from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_object_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        new_object = await self.session.execute(add_object_stmt)
        return new_object.scalars().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        await self.check_objects_count(**filter_by)

        update_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump())
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        await self.check_objects_count(**filter_by)

        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    async def check_objects_count(self, **filter_by) -> None:
        result = await self.session.execute(select(self.model).filter_by(**filter_by))
        result_count = len(result.scalars().all())

        if result_count > 1:
            raise HTTPException(status_code=422, detail="Найдено больше одного объектов")
        elif result_count == 0:
            raise HTTPException(status_code=404, detail="Не найдено ни одного объекта")
