from typing import TypeVar, Generic
import uuid as uuid_pkg
from abc import ABC, abstractmethod

from pymongo.errors import PyMongoError
from beanie.operators import Set

from app.models import Product, ProductType
from app.repositories.repositories_exceptions import DatabaseOperationError

DocumentType = TypeVar('DocumentType', bound=[Product, ProductType])


class BaseRepository(ABC, Generic[DocumentType]):
    def __init__(self, model: DocumentType):
        self._model = model

    @abstractmethod
    async def fetch_single_record(self, reference: uuid_pkg.UUID, **kwargs) -> DocumentType: ...

    @abstractmethod
    async def fetch(self, filter_data: dict,  **kwargs) -> list[DocumentType]: ...

    async def create(self, data: dict) -> DocumentType:
        try:
            db_object = await self._model(**data).insert()
            return db_object
        except PyMongoError as e:
            raise DatabaseOperationError(str(e)) from e

    async def update(self, reference_id: uuid_pkg.UUID, data: dict) -> DocumentType:
        try:
            entity = await self._model.get(reference_id)
            await entity.update(Set(data))
            return entity
        except PyMongoError as e:
            raise DatabaseOperationError(str(e)) from e

    async def delete(self, reference_id: uuid_pkg.UUID) -> None:
        try:
            entity = await self._model.get(reference_id)
            await entity.delete()
        except PyMongoError as e:
            raise DatabaseOperationError(str(e)) from e
