from typing import List
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from fastapi_utils.inferring_router import InferringRouter

from app.fastapi_utils.cbv import cbv
from app.storage.db import get_db
from app.fastapi_users import fastapi_users

from .statistics import router as stats_router
from .dependencies import TransactionFilterOptions
from .....storage.schemas.users import UserDB
from app import crud
from .....storage.schemas.transactions import TransactionOut, TransactionCreate, TransactionUpdate

router = InferringRouter()
router.include_router(stats_router)


class PaginatedTransaction(BaseModel):
    transactions: List[TransactionOut]
    total_transactions: int


class LegacyTransaction(BaseModel):
    date: datetime
    price: float
    comment: str
    incoming: bool


@cbv(router, prefix="/transactions", tags=["transactions"])
class TransactionCBV:

    user: UserDB = Depends(fastapi_users.get_current_active_user)
    db: AsyncSession = Depends(get_db)

    @router.get('')
    async def get_user_transactions(self, filter_options: TransactionFilterOptions = Depends()) -> PaginatedTransaction:

        transactions, total_transactions = await crud.transaction.get_multi_by_owner(
            db=self.db,
            user_id=self.user.id,
            **filter_options.dict(),
            get_total=True
        )

        return PaginatedTransaction(
            transactions=transactions,
            total_transactions=total_transactions
        )

    @router.get("/{id}")
    async def get_user_transaction(self, id: int) -> TransactionOut:

        existing_transaction = await crud.transaction.get_by_owner(db=self.db, id=id, user_id=self.user.id)
        if not existing_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return existing_transaction

    @router.post('')
    async def create_transaction(self, transaction_in: TransactionCreate) -> TransactionOut:

        new_transaction = await crud.transaction.create_with_owner(
            db=self.db,
            obj_in=transaction_in,
            user_id=self.user.id
        )

        return new_transaction

    @router.put("/{id}")
    async def update_transaction(self,
                                 id: int,
                                 transaction_in: TransactionUpdate) -> TransactionOut:

        existing_transaction = await crud.transaction.get_by_owner(db=self.db, id=id, user_id=self.user.id)
        if not existing_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        updated_transaction = await crud.transaction.update(
            db=self.db,
            db_obj=existing_transaction,
            obj_in=transaction_in
        )

        return updated_transaction

    @router.delete("/{id}")
    async def delete_transaction(self, id: int) -> TransactionOut:

        existing_transaction = await crud.transaction.get_by_owner(db=self.db, id=id, user_id=self.user.id)
        if not existing_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        removed_transaction = await crud.transaction.remove(db=self.db, id=id)
        return removed_transaction

    @router.post('/import/legacy')
    async def import_data(self, transactions_in: List[LegacyTransaction]) -> List[TransactionOut]:

        new_transactions = []
        for tx in transactions_in:
            price = tx.price if tx.incoming else -tx.price
            new_transaction = await crud.transaction.create_with_owner(
                db=self.db,
                obj_in=TransactionCreate(
                    price=price,
                    date=tx.date,
                    comment=tx.comment
                ),
                user_id=self.user.id
            )
            new_transactions.append(new_transaction)

        return new_transactions
