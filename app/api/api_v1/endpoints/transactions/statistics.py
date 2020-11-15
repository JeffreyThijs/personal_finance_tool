from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
from app.fastapi_users import fastapi_users

from app.crud import transaction
from .dependencies import DateFilters
from .....storage.schemas.users import UserDB
from .....storage.schemas.transactions import TransactionStatistics

router = APIRouter()


@router.get('', 
            response_model=TransactionStatistics, 
            summary="Global statistics of the transactions of a user")
def get_user_transactions_statistics(
        user: UserDB = Depends(fastapi_users.get_current_active_user),
        date_filters: DateFilters = Depends()):

    transactions = transaction.get_multi_by_owner(
        db=db.session,
        user_id=user.id,
        skip=None,
        limit=None,
        **date_filters.dict()
    )
    stats = TransactionStatistics(
        incoming=sum([t.price for t in transactions if t.price >= 0.0]),
        outgoing=-sum([t.price for t in transactions if t.price < 0.0])
    )

    return stats
