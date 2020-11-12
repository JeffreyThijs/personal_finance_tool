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
from ..settings import settings


database = Database(settings.DATABASE_URL)
Base: DeclarativeMeta = declarative_base()


class UserTable(Base, SQLAlchemyBaseUserTable):
    transactions = relationship("Transaction", backref="parent", cascade="all, delete")


class OAuthAccount(SQLAlchemyBaseOAuthAccountTable, Base):
    pass


users = UserTable.__table__
oauth_accounts = OAuthAccount.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users, oauth_accounts)


class TransactionTable(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    comment = Column(String, nullable=False)
    price = Column(Float, nullable=False)