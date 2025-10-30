from typing import Type

from fastapi import Depends

from app.repositories.product_repository import get_product_repository
from app.schemas.product_schemas import ProductOut, ProductIn

from app.repositories.product_repository import ProductRepository
from app.r_services.base import BaseService
from app.utils import MongoCriteriaFilter


class ProductService(BaseService[ProductIn, ProductOut]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)

    @property
    def _schema_out(self) -> Type[ProductOut]:
        return ProductOut

    def _build_search_criteria(self, filter_data: ProductIn) -> MongoCriteriaFilter:
        if filter_data.name:
            self._query_builder.add_text_search(filter_data.name)
        if filter_data.product_type:
            self._query_builder.add_nested_fields("product_type", filter_data.product_type)
        if filter_data.gt_price is not None:
            self._query_builder.add_greater_than("price", filter_data.gt_price)
        if filter_data.lt_price is not None:
            self._query_builder.add_less_than("price", filter_data.lt_price)
        if filter_data.quantity is not None:
            self._query_builder.add_exact_match("quantity", filter_data.quantity)
        return self._query_builder.build()


def get_product_service(repository: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repository)
