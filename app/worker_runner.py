import asyncio
import os
import signal
import sys

from app.config import get_worker_settings
from app.db_handler.async_db_handler import AsyncDatabaseClient
from app.db_sync.mq_client import get_async_mq_client
from app.db_sync.worker_factory import WorkerFactory
from app.r_services.service_factory import ServiceFactory


async def main(worker_type: str) -> None:
    settings = get_worker_settings()

    mongo_async_client = AsyncDatabaseClient(
        connection_string=settings.db_async_connection_string
    )

    async_mq_client = get_async_mq_client(
        settings=settings,
        worker_type=worker_type
    )

    worker_factory = WorkerFactory(
        async_mq_client=async_mq_client,
        service_factory=ServiceFactory(),
        async_mongo_client=mongo_async_client
    )

    worker = worker_factory.create_worker(worker_type=worker_type)

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda s=sig: worker.handle_shutdown_signal(s))

    await worker.sync_db()


if __name__ == "__main__":
    worker_type = os.getenv('WORKER_TYPE')

    if not worker_type:
        print("ERROR: WORKER_TYPE environment variable is not set")
        sys.exit(1)

    asyncio.run(main(worker_type=worker_type))
