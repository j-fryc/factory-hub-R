from app.db_handler.base import BaseDatabaseClient
from pymongo import MongoClient
from fastapi import Request


class SyncDatabaseClient(BaseDatabaseClient[MongoClient]):
    def _create_client(self) -> MongoClient:
        return MongoClient(
            self._connection_uri,
            maxPoolSize=self._max_pool_size,
            uuidRepresentation="standard"
        )


def get_sync_db_session(request: Request) -> MongoClient:
    return request.app.state.sync_db_handler.db_client
