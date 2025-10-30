from app.db_handler.base import BaseDatabaseClient
from pymongo import AsyncMongoClient
from fastapi import Request


class AsyncDatabaseClient(BaseDatabaseClient[AsyncMongoClient]):
    def _create_client(self) -> AsyncMongoClient:
        return AsyncMongoClient(
            self._connection_uri,
            maxPoolSize=self._max_pool_size,
            uuidRepresentation="standard"
        )


def get_sync_db_session(request: Request) -> AsyncMongoClient:
    return request.app.state.sync_db_handler.db_client
