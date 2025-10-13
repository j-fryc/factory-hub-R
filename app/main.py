from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.config import get_settings
from app.routers import r_router

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
    pass

app.include_router(r_router)
