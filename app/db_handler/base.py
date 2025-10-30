from abc import abstractmethod, ABC
from typing import TypeVar, Generic
from pymongo import MongoClient, AsyncMongoClient


ClientType = TypeVar("ClientType", bound=MongoClient | AsyncMongoClient)


class BaseDatabaseClient(ABC, Generic[ClientType]):
    def __init__(self, connection_string: str, pool_size: int = 20):
        self._connection_uri = connection_string
        self._max_pool_size = pool_size
        self._client = self._create_client()

    @abstractmethod
    def _create_client(self) -> ClientType: ...

    @property
    def db_client(self) -> ClientType:
        return self._client

