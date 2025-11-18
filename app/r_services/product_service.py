from typing import List

from fastapi import Depends
import uuid as uuid_pkg

from app.r_services.services_exceptions import DBException
from app.repositories.product_repository import get_product_repository
from app.repositories.repositories_exceptions import DatabaseOperationError
from app.schemas.product_schemas import ProductOut, ProductFetch, ProductCreate, ProductUpdate, ProductDelete

from app.repositories.product_repository import ProductRepository
from app.r_services.base import BaseService
from app.r_services.filter_builder import MongoCriteriaFilter


class ProductService(BaseService[ProductOut]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository=repository, output_schema=ProductOut)

    async def fetch_single_record(self, reference_id: uuid_pkg.UUID) -> ProductOut:
        try:
            fetched_data = await self._repository.fetch_single_record(reference=reference_id, fetch_related=True)
            return self._schema_out.model_validate(fetched_data)
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def fetch(self, filter_data: ProductFetch) -> List[ProductOut]:
        search_criteria = await self._build_search_criteria(data=filter_data)
        try:
            fetched_data_list = await self._repository.fetch(filter_data=search_criteria.query, fetch_related=True)
            return [self._schema_out.model_validate(fetched_data) for fetched_data in fetched_data_list]
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def update(self, data: ProductUpdate) -> ProductOut:
        return await super().update(data=data)
    
    async def delete(self, data: ProductDelete) -> None:
        return await super().delete(data=data)

    async def create(self, data: ProductCreate) -> ProductOut:
        return await super().create(data=data)

    async def _build_search_criteria(self, data: ProductFetch) -> MongoCriteriaFilter:
        if data.name:
            self._query_builder.add_text_search(data.name)
        if data.product_type_id:
            related_product_type = await self.fetch_single_record(reference_id=data.product_type_id)
            self._query_builder.add_nested_fields("product_type_id", related_product_type)
        if data.gt_price is not None:
            self._query_builder.add_greater_than("price", data.gt_price)
        if data.lt_price is not None:
            self._query_builder.add_less_than("price", data.lt_price)
        if data.quantity is not None:
            self._query_builder.add_exact_match("quantity", data.quantity)
        return self._query_builder.build()


def get_product_service(repository: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repository)
