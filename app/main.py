from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.api.v1 import api as api_v1
from app.core.config import config

logger.add(
    "./logs/s7.log",
    rotation="50 MB",
    retention=5,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager:
    """Логика запуска и завершения приложения."""

    yield


def _init_middlewares(app_: FastAPI) -> None:
    pass


def create_app() -> FastAPI:
    """Создает и возвращает экземпляр приложения FastAPI."""
    application = FastAPI(
        title=config.SERVICE_NAME,
        description=config.DESCRIPTION,
        debug=config.DEBUG,
        lifespan=lifespan,
    )

    _init_middlewares(application)

    application.include_router(api_v1.api_router, prefix=config.API_PATH)

    return application
