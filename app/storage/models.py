from databases import Database
from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyBaseOAuthAccountTable
)
from fastapi_users.db.sqlalchemy import GUID
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import func, Column, Float, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .mixins import TimestampMixin
from .schemas.users import UserDB
from ..settings import settings
from ..fastapi_users import SQLAlchemyUserDatabase


database = Database(settings.DATABASE_URL)
Base: DeclarativeMeta = declarative_base()


class UserTable(Base, SQLAlchemyBaseUserTable):
    transactions = relationship("TransactionTable", backref="parent", cascade="all, delete")


class OAuthAccount(SQLAlchemyBaseOAuthAccountTable, Base):
    pass


users = UserTable.__table__
oauth_accounts = OAuthAccount.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users, oauth_accounts)


class TransactionTable(Base, TimestampMixin):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    comment = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=func.now())
    
    user_id = Column(GUID, ForeignKey('user.id'))