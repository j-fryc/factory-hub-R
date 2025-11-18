import abc
from typing import TypeVar, Generic, List, Type
import uuid as uuid_pkg

from pydantic import BaseModel

from app.db_sync.exceptions import VersionConflictError, VersionLowerThenExpected
from app.r_services.services_exceptions import DBException
from app.repositories.base import BaseRepository
from app.repositories.repositories_exceptions import DatabaseOperationError
from app.r_services.filter_builder import MongoCriteriaFilterBuilder
from app.schemas.base_schemas import FetchDTO, CreateDTO, UpdateDTO, DeleteDTO


OutputDTOSchema = TypeVar('OutputDTOSchema', bound=BaseModel)


class BaseService(abc.ABC, Generic[OutputDTOSchema]):
    def __init__(self, repository: BaseRepository, output_schema: Type[OutputDTOSchema]):
        self._repository = repository
        self._query_builder = MongoCriteriaFilterBuilder()
        self._schema_out = output_schema

    async def fetch_single_record(self, reference_id: uuid_pkg.UUID) -> OutputDTOSchema:
        try:
            fetched_data = await self._repository.fetch_single_record(reference=reference_id)
            return self._schema_out.model_validate(fetched_data)
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def fetch(self, filter_data: FetchDTO) -> List[OutputDTOSchema]:
        search_criteria = await self._build_search_criteria(data=filter_data)
        try:
            fetched_data_list = await self._repository.fetch(filter_data=search_criteria.query)
            return [self._schema_out.model_validate(fetched_data) for fetched_data in fetched_data_list]
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def update(self, data: UpdateDTO) -> OutputDTOSchema:
        try:
            await self._verify_aggregate_version(
                reference_id=data.id,
                expected_version=data.entity_version
            )
            updated_document = await self._repository.update(
                reference_id=data.id,
                data=data.model_dump(
                    exclude={'id'},
                    exclude_none=True
                )
            )
            return self._schema_out.model_validate(updated_document)
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def delete(self, data: DeleteDTO) -> None:
        try:
            await self._verify_aggregate_version(
                reference_id=data.id,
                expected_version=data.entity_version
            )
            await self._repository.delete(reference_id=data.id)
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def create(self, data: CreateDTO) -> OutputDTOSchema:
        try:
            added_document = await self._repository.create(data=data.model_dump())
            return self._schema_out.model_validate(added_document)
        except DatabaseOperationError as e:
            raise DBException(e) from e

    async def _verify_aggregate_version(self, reference_id: uuid_pkg.UUID, expected_version: int) -> None:
        if expected_version is None:
            raise ValueError("Missing version in payload")

        current = await self.fetch_single_record(reference_id)
        if not current or current.entity_version + 1 < expected_version:
            raise VersionConflictError(
                f"Expected {expected_version}, got {current.entity_version}"
            )
        elif current.entity_version + 1 > expected_version:
            raise VersionLowerThenExpected(
                f"Expected {expected_version} is lower than {current.entity_version}, something is wrong!"
            )

    @abc.abstractmethod
    async def _build_search_criteria(self, data: BaseModel):
        raise NotImplementedError
