from fastapi import APIRouter, Depends, Query
from fastapi_sqlalchemy import db
from app.fastapi_users import fastapi_users

from app.crud import transaction
from .....storage.schemas.users import UserDB
from .....storage.schemas.transactions import TransactionStatistics

router = APIRouter()


@router.get('', response_model=TransactionStatistics, summary="Global statistics of the transactions of a user")
def get_user_transactions_statistics(
        user: UserDB = Depends(fastapi_users.get_current_active_user),
        year: int = Query(None, title="The year of the month to get the stats from", ge=1900, le=3000), 
        month: int = Query(None, title="The month numerically to get the stats from", ge=1, le=12)):

    transactions = transaction.get_multi_by_owner(db=db.session, user_id=user.id, month=month, year=year)
    stats = TransactionStatistics(
        incoming=sum([t.price for t in transactions if t.price >= 0.0]),
        outgoing=-sum([t.price for t in transactions if t.price < 0.0])
    )
    return stats