from typing import List, Union
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_utils.inferring_router import InferringRouter

from app.fastapi_users import fastapi_users
from app.fastapi_utils.cbv import cbv
from app.storage.db import get_db
from app import crud

from .dependencies import PartitionFunction, PartitionalDateFilters
from .....storage.schemas.users import UserDB
from .....storage.schemas.transactions import TransactionStatistics, TransactionStatisticsByMonth

router = InferringRouter()


@cbv(router, prefix="/stats", tags=["statistics", "transactions"])
class TransactionCBV:

    user: UserDB = Depends(fastapi_users.get_current_active_user)
    db: AsyncSession = Depends(get_db)

    @router.get('', summary="Global statistics of the transactions of a user")
    async def get_user_transactions_statistics(
        self,
        date_filters: PartitionalDateFilters = Depends(),
    ) -> Union[TransactionStatistics, List[TransactionStatisticsByMonth]]:

        transactions = await crud.transaction.get_multi_by_owner(
            db=self.db,
            user_id=self.user.id,
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
            if date_filters.partition_func == PartitionFunction.by_month:
                stats = []
                for (year, month), txs in transactions:
                    incoming, outgoing = [], []
                    for t in txs:
                        (incoming, outgoing)[t.price < 0].append(t.price)
                    stat = TransactionStatisticsByMonth(
                        year=year,
                        month=month,
                        incoming=sum(incoming),
                        outgoing=-sum(outgoing)
                    )
                    stats.append(stat)
            else:
                raise NotImplementedError()

        return stats
