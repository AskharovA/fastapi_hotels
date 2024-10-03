from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter_, **filter_by):
        query = (
            select(self.model)
            .filter(*filter_)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        add_object_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        new_object = await self.session.execute(add_object_stmt)
        model = new_object.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        await self.check_objects_count(**filter_by)

        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
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
