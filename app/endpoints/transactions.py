from fastapi import APIRouter, Depends
from ..users import fastapi_users

from ..storage.schemas.users import UserDB
from ..storage.schemas.transactions import TransactionDB

router = APIRouter()

@router.get('/transactions')
def transactions(user: UserDB = Depends(fastapi_users.get_current_active_user)):
    
    transactions = [
         TransactionDB(
            price=22.66,
            comment="beer",
            id="1234"
        )
    ]
    
    return {
        "transactions": transactions
    }