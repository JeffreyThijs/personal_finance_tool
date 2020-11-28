import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from ..settings import settings

logger = logging.getLogger(__name__)

print(settings.ASYNC_DATABASE_URL)
try:
    engine = create_async_engine(
        settings.ASYNC_DATABASE_URL
    )
except Exception as e:
    from sqlalchemy import create_engine
    logger.critical("could not load async engine, trying again with non async engine...")
    engine = create_engine(settings.DATABASE_URL)
    

async def get_db() -> AsyncSession:
    """ FastAPI dependency that provides a sqlalchemy session """
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()
