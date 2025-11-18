from aio_pika.abc import AbstractIncomingMessage
from beanie import init_beanie
from pydantic import ValidationError

from app.db_handler.async_db_handler import AsyncDatabaseClient
from app.db_sync.exceptions import VersionConflictError, VersionLowerThenExpected
from app.db_sync.mq_client import AsyncMQClient
from app.models import Product, ProductType
from app.r_services.base import BaseService
from app.repositories.repositories_exceptions import NotFoundError
from app.schemas.db_sync_schema import OutboxEventDTO, AggregateType

import warnings


class DBSyncWorker:
    def __init__(self, service: BaseService, async_mq_client: AsyncMQClient, async_mongo_client: AsyncDatabaseClient):
        self._service = service
        self._async_mq_client = async_mq_client
        self._service_action_registry = {
            AggregateType.CREATE: self._service.create,
            AggregateType.UPDATE: self._service.update,
            AggregateType.DELETE: self._service.delete
        }
        self._async_mongo_client = async_mongo_client

    async def handle_shutdown_signal(self, sig_name: str):
        await self._async_mq_client.disconnect()

    async def sync_db(self):
        async def operation_strategy(message: AbstractIncomingMessage):
            validated_data = OutboxEventDTO.model_validate_json(message.body)
            try:
                await self._service_action_registry[validated_data.event_type](validated_data.payload)
            except (VersionConflictError, NotFoundError):
                await self._async_mq_client.publish_data(msg=message.body, dead_letter_queue=True)
            except (VersionLowerThenExpected, ValidationError) as e:
                warnings.warn(f"{str(e)}, skipping operation")
            finally:
                await message.ack()

        await init_beanie(
            database=self._async_mongo_client.db_client.get_database(),
            document_models=[Product, ProductType]
        )
        await self._async_mq_client.connect()
        await self._async_mq_client.consume_data(operation_strategy)
