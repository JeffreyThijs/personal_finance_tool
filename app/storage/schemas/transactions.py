from typing import List, Set
from pydantic import BaseModel, validator
from pydantic.types import conint
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from ..models import TransactionTable as Transaction

_TransactionDB = sqlalchemy_to_pydantic(Transaction)
_TransactionCreate = sqlalchemy_to_pydantic(
    Transaction, exclude=["id", "user_id", "updated_at", "created_at"])
_TransactionUpdate = sqlalchemy_to_pydantic(
    Transaction, exclude=["id", "user_id", "updated_at", "created_at"])
_TransactionOut = sqlalchemy_to_pydantic(
    Transaction, exclude=["user_id", "updated_at", "created_at"])


class TransactionDB(_TransactionDB):
    pass


class TransactionCreate(_TransactionCreate):
    tags: Set[str]


class TransactionUpdate(_TransactionUpdate):
    tags: Set[str]


class TransactionOut(_TransactionOut):
    tags: Set[str]


class TransactionStatistics(BaseModel):
    incoming: float = 0
    outgoing: float = 0
    balance: float = None

    @validator("balance", always=True)
    def balance_calc(cls, v, values, **kwargs):
        return values.get("incoming", 0) - values.get("outgoing", 0)


class TransactionStatisticsByMonth(TransactionStatistics):
    month: conint(gt=0, lt=13)
    year: conint(gt=1999, lt=3001)
