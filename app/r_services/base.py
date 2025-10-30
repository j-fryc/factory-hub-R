import abc
from typing import TypeVar, Generic, Type

from sqlalchemy.exc import SQLAlchemyError

from app.r_services.services_exceptions import DBException
from app.repositories.base import BaseRepository
from app.repositories.repositories_exceptions import DatabaseOperationError
from app.schemas.product_schemas import ProductIn, ProductOut
from app.schemas.product_type_schemas import ProductTypeIn, ProductTypeOut
from app.utils import MongoCriteriaFilterBuilder

ModelTypeIn = TypeVar("ModelTypeIn", bound=[ProductIn, ProductTypeIn])
ModelTypeOut = TypeVar("ModelTypeOut", bound=[ProductOut, ProductTypeOut])


class BaseService(abc.ABC, Generic[ModelTypeIn, ModelTypeOut]):
    def __init__(self, repository: BaseRepository):
        self._repository = repository
        self._query_builder = MongoCriteriaFilterBuilder()

    async def fetch_single_record(self, reference_id: str) -> ModelTypeOut:
        try:
            fetched_data = await self._repository.fetch_single_record(reference=reference_id)
            return self._schema_out.model_validate(fetched_data)
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def fetch(self, filter_data: ModelTypeIn):
        try:
            search_criteria = self._build_search_criteria(filter_data)
            fetched_data_list = await self._repository.fetch(filter_data=search_criteria.query)
            return [self._schema_out.model_validate(fetched_data) for fetched_data in fetched_data_list]
        except DatabaseOperationError as e:
            raise DBException(e) from e

    @abc.abstractmethod
    def _build_search_criteria(self, filter_data: ModelTypeIn):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _schema_out(self) -> Type[ModelTypeOut]:
        raise NotImplementedError
