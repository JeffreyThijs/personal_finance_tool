from datetime import datetime
from pydantic.main import BaseModel
from pydantic import UUID4 as GUID
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
# from ..models import TransactionTable as Transaction

class BaseTransaction(BaseModel):
    date: datetime
    comment: str
    price: float
    
class BaseTransactionWithId(BaseTransaction):
    id: int
    
class TransactionDB(BaseTransactionWithId):
    created_at: datetime
    updated_at: datetime
    user_id: GUID
    
class TransactionCreate(BaseTransaction):
    pass

class TransactionUpdate(BaseTransaction):
    pass

class TransactionOut(BaseTransactionWithId):
    
    class Config:
        orm_mode = True
    

# TransactionDB = sqlalchemy_to_pydantic(Transaction)
# TransactionCreate = sqlalchemy_to_pydantic(Transaction, exclude=["id", "user_id", "updated_at", "created_at"])
# TransactionUpdate = sqlalchemy_to_pydantic(Transaction, exclude=["id", "user_id", "updated_at", "created_at"])
# TransactionOut = sqlalchemy_to_pydantic(Transaction, exclude=["id", "user_id", "updated_at", "created_at"])