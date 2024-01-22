import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from social_media_api.database import database
from social_media_api.logging_conf import configure_logging
from social_media_api.routers.post import router as post_router
from social_media_api.routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(post_router)
app.include_router(user_router)


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logging.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
