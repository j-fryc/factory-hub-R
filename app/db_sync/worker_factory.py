from app.db_handler.async_db_handler import AsyncDatabaseClient
from app.db_sync.db_sync_worker import DBSyncWorker
from app.db_sync.mq_client import AsyncMQClient
from app.r_services.service_factory import ServiceFactory
from app.schemas.db_sync_schema import WorkerTypeValue


class WorkerFactory:
    def __init__(
            self,
            async_mq_client: AsyncMQClient,
            service_factory: ServiceFactory,
            async_mongo_client: AsyncDatabaseClient
    ):
        self._service_factory = service_factory
        self._async_mq_client = async_mq_client
        self._async_mongo_client = async_mongo_client

    def create_worker(self, worker_type: WorkerTypeValue):
        return DBSyncWorker(
            async_mq_client=self._async_mq_client,
            service=self._service_factory.create_service(
                worker_type=worker_type
            ),
            async_mongo_client=self._async_mongo_client
        )
