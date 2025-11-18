from typing import List

from fastapi import Depends
import uuid as uuid_pkg

from app.r_services.services_exceptions import DBException
from app.repositories.repositories_exceptions import DatabaseOperationError
from app.schemas.product_type_schemas import ProductTypeOut, ProductTypeFetch, ProductTypeCreate, ProductTypeDelete, \
    ProductTypeUpdate

from app.repositories.product_type_repository import ProductTypeRepository, get_product_type_repository
from app.r_services.base import BaseService

from app.r_services.filter_builder import MongoCriteriaFilter


class ProductTypeService(BaseService[ProductTypeOut]):
    def __init__(self, repository: ProductTypeRepository):
        super().__init__(repository=repository, output_schema=ProductTypeOut)

    async def fetch_single_record(self, reference_id: uuid_pkg.UUID) -> ProductTypeOut:
        try:
            fetched_data = await self._repository.fetch_single_record(reference=reference_id)
            return self._schema_out.model_validate(fetched_data)
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def fetch(self, filter_data: ProductTypeFetch) -> List[ProductTypeOut]:
        search_criteria = await self._build_search_criteria(data=filter_data)
        try:
            fetched_data_list = await self._repository.fetch(filter_data=search_criteria.query)
            return [self._schema_out.model_validate(fetched_data) for fetched_data in fetched_data_list]
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def update(self, data: ProductTypeUpdate) -> ProductTypeOut:
        return await super().update(data=data)

    async def delete(self, data: ProductTypeDelete) -> None:
        return await super().delete(data=data)

    async def create(self, data: ProductTypeCreate) -> ProductTypeOut:
        return await super().create(data=data)

    async def _build_search_criteria(self, data: ProductTypeFetch) -> MongoCriteriaFilter:
        if data.name:
            self._query_builder.add_exact_match("name", data.name)
        if data.description:
            self._query_builder.add_text_search(data.description)
        return self._query_builder.build()


def get_product_type_service(repository: ProductTypeRepository = Depends(get_product_type_repository)) -> ProductTypeService:
    return ProductTypeService(repository=repository)
