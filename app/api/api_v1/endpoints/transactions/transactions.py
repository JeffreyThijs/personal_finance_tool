from typing import List
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from app.storage.db import get_db
from app.fastapi_users import fastapi_users

from .statistics import router as stats_router
from .dependencies import TransactionFilterOptions
from .....storage.schemas.users import UserDB
from app import crud
from .....storage.schemas.transactions import TransactionOut, TransactionCreate, TransactionUpdate

router = APIRouter()
router.include_router(stats_router, prefix="/stats", tags=["statistics"])


class PaginatedTransaction(BaseModel):
    transactions: List[TransactionOut]
    total_transactions: int


class LegacyTransaction(BaseModel):
    date: datetime
    price: float
    comment: str
    incoming: bool


@router.get('', response_model=PaginatedTransaction)
async def get_user_transactions(user: UserDB = Depends(fastapi_users.get_current_active_user),
                                filter_options: TransactionFilterOptions = Depends(),
                                db: AsyncSession = Depends(get_db)):

    transactions, total_transactions = await crud.transaction.get_multi_by_owner(
        db=db,
        user_id=user.id,
        **filter_options.dict(),
        get_total=True
    )

    return PaginatedTransaction(
        transactions=transactions,
        total_transactions=total_transactions
    )


@router.get("/{id}", response_model=TransactionOut)
async def get_user_transaction(id: int,
                               user: UserDB = Depends(fastapi_users.get_current_active_user),
                               db: AsyncSession = Depends(get_db)):

    existing_transaction = await crud.transaction.get_by_owner(db=db, id=id, user_id=user.id)
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return existing_transaction


@router.post('', response_model=TransactionOut)
async def create_transaction(transaction_in: TransactionCreate,
                             user: UserDB = Depends(fastapi_users.get_current_active_user),
                             db: AsyncSession = Depends(get_db)):

    new_transaction = await crud.transaction.create_with_owner(
        db=db,
        obj_in=transaction_in,
        user_id=user.id
    )

    return new_transaction


@router.put("/{id}", response_model=TransactionOut)
async def update_transaction(id: int,
                             transaction_in: TransactionUpdate,
                             user: UserDB = Depends(fastapi_users.get_current_active_user),
                             db: AsyncSession = Depends(get_db)):

    existing_transaction = await crud.transaction.get_by_owner(db=db, id=id, user_id=user.id)
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    updated_transaction = await crud.transaction.update(
        db=db,
        db_obj=existing_transaction,
        obj_in=transaction_in
    )

    return updated_transaction


@router.delete("/{id}", response_model=TransactionOut)
async def delete_transaction(id: int,
                             user: UserDB = Depends(fastapi_users.get_current_active_user),
                             db: AsyncSession = Depends(get_db)):

    existing_transaction = await crud.transaction.get_by_owner(db=db, id=id, user_id=user.id)
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    removed_transaction = await crud.transaction.remove(db=db, id=id)
    return removed_transaction


@router.post('/import/legacy', response_model=List[TransactionOut])
async def import_data(transactions_in: List[LegacyTransaction],
                      user: UserDB = Depends(fastapi_users.get_current_active_user),
                      db: AsyncSession = Depends(get_db)):

    new_transactions = []
    for tx in transactions_in:
        price = tx.price if tx.incoming else -tx.price
        new_transaction = await crud.transaction.create_with_owner(
            db=db,
            obj_in=TransactionCreate(
                price=price,
                date=tx.date,
                comment=tx.comment
            ),
            user_id=user.id
        )
        new_transactions.append(new_transaction)

    return new_transactions
