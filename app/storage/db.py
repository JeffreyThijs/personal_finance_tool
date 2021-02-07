import logging
from typing import Union
from functools import lru_cache
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from ..settings import get_settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=2)
def get_engine() -> Union[AsyncEngine, Engine]:
    settings = get_settings()
    engine_options = dict(pool_size=settings.MAX_DB_SESSIONS, max_overflow=2)
    try:
        engine = create_async_engine(settings.ASYNC_DATABASE_URL, **engine_options)
    except Exception as e:
        from sqlalchemy import create_engine
        logger.critical(
            "could not load async engine, trying again with non async engine...")
        engine = create_engine(settings.DATABASE_URL, **engine_options)

    return engine


async def get_db() -> AsyncSession:
    """ FastAPI dependency that provides a sqlalchemy session """
    engine = get_engine()
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()
