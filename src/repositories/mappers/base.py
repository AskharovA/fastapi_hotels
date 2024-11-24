from typing import Type, TypeVar, Any

from pydantic import BaseModel
from sqlalchemy import Row, RowMapping

from src.database import Base

# SchemaType = TypeVar("SchemaType", bound=BaseModel)
# ModelType = TypeVar("ModelType", bound=Base)


class DataMapper:
    db_model: type[Base]
    schema: type[BaseModel]

    @classmethod
    def map_to_domain_entity(cls, data: Row | RowMapping | Any) -> BaseModel:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: BaseModel) -> Base:
        return cls.db_model(**data.model_dump())
