from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.v1 import api as api_v1
from app.core.config import config
from app.db.database import engine, Base

logger.add(
    "./logs/s7.log",
    rotation="50 MB",
    retention=5,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager:
    """Логика запуска и завершения приложения."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


def _init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


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
