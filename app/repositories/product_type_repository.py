import uuid as uuid_pkg

from pymongo.errors import PyMongoError

from app.models import ProductType
from app.repositories.base import BaseRepository
from app.repositories.repositories_exceptions import NotFoundError, DatabaseOperationError


class ProductTypeRepository(BaseRepository[ProductType]):
    def __init__(self):
        super().__init__(ProductType)

    async def fetch_single_record(self, reference: uuid_pkg.UUID, **kwargs) -> ProductType:
        try:
            entity = await self._model.get(reference)
            if entity is None:
                raise NotFoundError(reference)
            return entity
        except PyMongoError as e:
            raise DatabaseOperationError(str(e)) from e

    async def fetch(self, filter_data: dict, **kwargs) -> list[ProductType]:
        try:
            entities = await self._model.find(filter_data).to_list()
            if not entities:
                raise NotFoundError(filter_data)
            return entities
        except PyMongoError as e:
            raise DatabaseOperationError(str(e)) from e


def get_product_type_repository() -> ProductTypeRepository:
    return ProductTypeRepository()
