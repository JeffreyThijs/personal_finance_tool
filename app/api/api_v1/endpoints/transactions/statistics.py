from typing import List, Union
from app.storage.models import TransactionTable
from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db
from app.fastapi_users import fastapi_users

from app.crud import transaction
from .dependencies import DateFilters, PartitionFunction, PartitionaleDateFilters
from .....storage.schemas.users import UserDB
from .....storage.schemas.transactions import TransactionStatistics, TransactionStatisticsByMonth

router = APIRouter()


@router.get('', 
            response_model=Union[TransactionStatistics, List[TransactionStatisticsByMonth]], 
            summary="Global statistics of the transactions of a user")
def get_user_transactions_statistics(
        user: UserDB = Depends(fastapi_users.get_current_active_user),
        date_filters: PartitionaleDateFilters = Depends()):
    
    transactions = transaction.get_multi_by_owner(
        db=db.session,
        user_id=user.id,
        skip=None,
        limit=None,
        **date_filters.dict()
    )
    
    if isinstance(transactions, list):
        stats = TransactionStatistics(
            incoming=sum([t.price for t in transactions if t.price >= 0.0]),
            outgoing=-sum([t.price for t in transactions if t.price < 0.0])
        )
    else:
        print(date_filters.partition_func)
        if date_filters.partition_func == PartitionFunction.by_month:
            stats = []
            for (year, month), txs in transactions:
                stat = TransactionStatisticsByMonth(
                    year=year,
                    month=month,
                    incoming=sum(t.price for t in txs if t.price >= 0),
                    outgoing=sum(t.price for t in txs if t.price < 0)
                )
                stats.append(stat)
        else:
            raise NotImplementedError()

    return stats