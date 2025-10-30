from typing import TypeVar, Generic

from pymongo.errors import PyMongoError

from app.models import Product, ProductType
from app.repositories.repositories_exceptions import DatabaseOperationError, NotFoundError


DocumentType = TypeVar('DocumentType', bound=[Product, ProductType])


class BaseRepository(Generic[DocumentType]):
    def __init__(self, model: DocumentType):
        self._model = model

    async def fetch_single_record(self, reference: str) -> DocumentType:
        try:
            entity = await self._model.get(reference, fetch_links=True)
            if entity is None:
                raise NotFoundError(reference)
            return entity
        except PyMongoError as e:
            raise DatabaseOperationError(str(e)) from e

    async def fetch(self, filter_data: dict) -> list[DocumentType]:
        try:
            entities = await self._model.find(filter_data, fetch_links=True).to_list()
            if not entities:
                raise NotFoundError(filter_data)
            return entities
        except PyMongoError as e:
            raise DatabaseOperationError(str(e)) from e
