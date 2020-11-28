from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from ..settings import settings

engine = create_async_engine(
    settings.ASYNC_DATABASE_URL
)

async def get_db() -> AsyncSession:
    """ FastAPI dependency that provides a sqlalchemy session """
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()
