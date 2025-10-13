from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    secret_key: str
    mongo_db_host: str = Field(alias="MONGO_DB_HOST")
    mongo_db_port: str = Field(alias="MONGO_DB_PORT")
    mongo_db_user: str = Field(alias="MONGO_DB_ROOT_USER")
    mongo_db_password: str = Field(alias="MONGO_DB_ROOT_PASS")
    rabbitmq_host: str = Field(alias="RABBITMQ_HOST")
    rabbitmq_port: int = Field(alias="RABBITMQ_PORT")
    rabbitmq_user: str = Field(alias="RABBITMQ_USER")
    rabbitmq_password: str = Field(alias="RABBITMQ_PASSWORD")
    rabbitmq_vhost: str = Field(alias="RABBITMQ_VHOST")
    rabbitmq_queue: str = Field(alias="RABBITMQ_QUEUE")
    rabbitmq_exchange: str = Field(alias="RABBITMQ_EXCHANGE")
    rabbitmq_routing_key: str = Field(alias="RABBITMQ_ROUTING_KEY")

    class Config:
        env_file = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
