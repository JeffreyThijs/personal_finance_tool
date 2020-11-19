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
    pass


class TransactionUpdate(_TransactionUpdate):
    pass


class TransactionOut(_TransactionOut):
    pass


class TransactionStatistics(BaseModel):
    incoming: float
    outgoing: float
    balance: float = None

    @validator("balance", always=True)
    def balance_calc(cls, v, values, **kwargs):
        return values["incoming"] - values["outgoing"]


class TransactionStatisticsByMonth(TransactionStatistics):
    month: conint(gt=0, lt=13)
    year: conint(gt=1999, lt=3001)
