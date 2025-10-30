from typing import Type

from fastapi import Depends

from app.schemas.product_type_schemas import ProductTypeOut, ProductTypeIn

from app.repositories.product_type_repository import ProductTypeRepository, get_product_type_repository
from app.r_services.base import BaseService

from app.utils import MongoCriteriaFilter


class ProductTypeService(BaseService[ProductTypeIn, ProductTypeOut]):
    def __init__(self, repository: ProductTypeRepository):
        super().__init__(repository)

    @property
    def _schema_out(self) -> Type[ProductTypeOut]:
        return ProductTypeOut

    def _build_search_criteria(self, filter_data: ProductTypeIn) -> MongoCriteriaFilter:
        if filter_data.type_name:
            self._query_builder.add_exact_match("type_name", filter_data.type_name)
        if filter_data.description:
            self._query_builder.add_text_search(filter_data.description)
        return self._query_builder.build()


def get_product_type_service(repository: ProductTypeRepository = Depends(get_product_type_repository)) -> ProductTypeService:
    return ProductTypeService(repository=repository)
