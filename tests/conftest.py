from typing import Iterator
import pytest
import tempfile

from pytest_postgresql import factories
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

socket_dir = tempfile.TemporaryDirectory()
postgresql_my_proc = factories.postgresql_proc(port=None, unixsocketdir=socket_dir.name)
postgresql_my = factories.postgresql('postgresql_my_proc')

@pytest.fixture(scope='function')
async def db_session(postgresql_my) -> Iterator[AsyncSession]:
    """Session for SQLAlchemy."""
    from app.storage.models import Base

    def db_creator():
        return postgresql_my.cursor().connection

    engine = create_async_engine('postgresql+psycopg2://', creator=db_creator)
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)    
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()
