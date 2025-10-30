from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    secret_key: str
    db_async_connection_string: str = Field(alias="MONGO_DB_CONNECTION_STRING")
    db_sync_connection_string: str = Field(alias="MONGO_DB_CONNECTION_STRING")

    class Config:
        env_file = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
