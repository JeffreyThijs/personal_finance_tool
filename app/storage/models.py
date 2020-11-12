from databases import Database
from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyBaseOAuthAccountTable
)
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from .monkey_patches import SQLAlchemyUserDatabase
from .schemas import UserDB
from ..config import Config


config = Config.from_environ()
database = Database(config.DATABASE_URL)
Base: DeclarativeMeta = declarative_base()


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass


class OAuthAccount(SQLAlchemyBaseOAuthAccountTable, Base):
    pass


users = UserTable.__table__
oauth_accounts = OAuthAccount.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users, oauth_accounts)
