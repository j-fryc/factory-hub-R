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


class WorkerSettings(BaseSettings):
    rabbit_mq_exchange_name: str = Field(alias="RABBIT_MQ_EXCHANGE_NAME")
    rabbit_mq_exchange_name_dlx: str = Field(alias="RABBIT_MQ_EXCHANGE_NAME_DLX")
    rabbit_mq_host: str = Field(alias="RABBIT_MQ_HOST")
    rabbit_mq_port: int = Field(alias="RABBIT_MQ_PORT")
    rabbit_mq_user: str = Field(alias="RABBIT_MQ_USER")
    rabbit_mq_password: str = Field(alias="RABBIT_MQ_PASSWORD")
    db_async_connection_string: str = Field(alias="MONGO_DB_CONNECTION_STRING")
    delay_ms_dlx: int = Field(alias="DELAY_MS_DLX")

    class Config:
        env_file = None


@lru_cache
def get_worker_settings() -> WorkerSettings:
    return WorkerSettings()
