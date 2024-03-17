from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

from app.core.config import config

engine = create_async_engine(config.POSTGRES_URI, echo=False)


async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

metadata = MetaData()

Base = declarative_base(metadata=metadata)
