from typing import Iterator
from databases import Database
from functools import lru_cache
from sqlalchemy.orm import Session
from fastapi_utils.session import FastAPISessionMaker


from .schemas.users import UserDB
from ..settings import settings
from ..fastapi_users import SQLAlchemyUserDatabase
from .models import UserTable, OAuthAccount, Base

users = UserTable.__table__
oauth_accounts = OAuthAccount.__table__

database = Database(settings.DATABASE_URL, min_size=2, max_size=5)
user_db = SQLAlchemyUserDatabase(UserDB, database, users, oauth_accounts)


def get_db() -> Iterator[Session]:
    """ FastAPI dependency that provides a sqlalchemy session """
    yield from _get_fastapi_sessionmaker().get_db()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    """ This function could be replaced with a global variable if preferred """
    return FastAPISessionMaker(settings.DATABASE_URL)

def get_db() -> Iterator[Session]:
    """ FastAPI dependency that provides a sqlalchemy session """
    yield from _get_fastapi_sessionmaker().get_db()