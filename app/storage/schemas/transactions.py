from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from ..models import TransactionTable

TransactionDB = sqlalchemy_to_pydantic(TransactionTable)