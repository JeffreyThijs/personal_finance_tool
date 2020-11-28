from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyBaseOAuthAccountTable
)
from fastapi_users.db.sqlalchemy import GUID
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    func,
    Column,
    Float,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from .mixins import TimestampMixin

Base = declarative_base()


class UserTable(Base, SQLAlchemyBaseUserTable):
    transactions = relationship("TransactionTable", backref="parent", cascade="all, delete")


class OAuthAccount(SQLAlchemyBaseOAuthAccountTable, Base):
    pass


class TransactionTable(Base, TimestampMixin):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    comment = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=func.now())

    user_id = Column(GUID, ForeignKey('user.id'))

    tags = Column(ARRAY(String))
