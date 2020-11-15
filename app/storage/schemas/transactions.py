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
