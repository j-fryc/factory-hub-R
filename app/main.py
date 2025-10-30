from beanie import init_beanie
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.config import get_settings
from app.db_handler.async_db_handler import AsyncDatabaseClient
from app.db_handler.sync_db_handler import SyncDatabaseClient
from app.models import Product, ProductType
from app.routers import r_router, sync_router

app = FastAPI()

settings = get_settings()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie="fastapi_session",
    max_age=3600,
)

@app.on_event("startup")
async def startup():
    async_db_client = AsyncDatabaseClient(
        connection_string=settings.db_async_connection_string
    )
    sync_db_client = SyncDatabaseClient(
        connection_string=settings.db_sync_connection_string
    )
    await init_beanie(database=async_db_client.db_client.get_database(), document_models=[Product, ProductType])
    # app.state.async_db_handler = async_db_handler
    # app.state.sync_db_handler = sync_db_handler

app.include_router(r_router)
app.include_router(sync_router)
