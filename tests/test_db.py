import asyncio
import pytest
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import uuid4
from app.storage.models import UserTable
from fastapi_users.password import get_password_hash

fake = Faker()

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_db(db_session: AsyncSession):
    user = UserTable(
                    id=uuid4(),
                    email=fake.ascii_company_email(),
                    hashed_password=get_password_hash(fake.password(length=12)),
                )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    db_exectute = await db_session.execute(select(UserTable).filter(UserTable.id == user.id))
    query_user = db_exectute.scalar_one_or_none()
    
    assert query_user.id == user.id