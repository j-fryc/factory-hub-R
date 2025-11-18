from pymongo.errors import PyMongoError
import uuid as uuid_pkg

from app.models import Product
from app.repositories.base import BaseRepository
from app.repositories.repositories_exceptions import DatabaseOperationError, NotFoundError


class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)

    async def fetch_single_record(self, reference: uuid_pkg.UUID, fetch_related: bool = False, **kwargs) -> Product:
        try:
            if fetch_related:
                pipeline = [
                    {"$match": {"_id": reference}},
                    {
                        "$lookup": {
                            "from": "ProductType",
                            "localField": "product_type_id",
                            "foreignField": "_id",
                            "as": "product_type"
                        }
                    },
                    {
                        "$unwind": {
                            "path": "$product_type",
                            "preserveNullAndEmptyArrays": True
                        }
                    },
                    {
                        "$set": {
                            "id": "$_id",
                            "product_type.id": "$product_type._id"
                        }
                    },
                    {
                        "$unset": ["_id", "product_type._id"]
                    }
                ]
                result = await self._model.aggregate(pipeline).to_list(length=1)
                if not result:
                    raise NotFoundError(reference)
                entity = result[0]
            else:
                entity = await self._model.get(reference)
                if entity is None:
                    raise NotFoundError(reference)

            return entity
        except PyMongoError as e:
            raise DatabaseOperationError(str(e)) from e

    async def fetch(self, filter_data: dict, fetch_related: bool = False, **kwargs) -> list[Product]:
        try:
            if fetch_related:
                pipeline = [
                    {"$match": filter_data},
                    {
                        "$lookup": {
                            "from": "ProductType",
                            "localField": "product_type_id",
                            "foreignField": "_id",
                            "as": "product_type"
                        }
                    },
                    {
                        "$unwind": {
                            "path": "$product_type",
                            "preserveNullAndEmptyArrays": True
                        }
                    },
                    {
                        "$set": {
                            "id": "$_id",
                            "product_type.id": "$product_type._id"
                        }
                    },
                    {
                        "$unset": ["_id", "product_type._id"]
                    }
                ]
                entities = await self._model.aggregate(pipeline).to_list()
            else:
                entities = await self._model.find(filter_data).to_list()

            if not entities:
                raise NotFoundError(filter_data)

            return entities
        except PyMongoError as e:
            raise DatabaseOperationError(str(e)) from e


def get_product_repository() -> ProductRepository:
    return ProductRepository()
