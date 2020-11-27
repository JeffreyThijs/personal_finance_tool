from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic.main import BaseModel
from app.fastapi_users import fastapi_users

from app.storage.db import Session, get_db
from .statistics import router as stats_router
from .dependencies import DateFilters, TransactionSortBy, TransactionTypeFilters
from ..dependencies import PaginationParams
from .....storage.schemas.users import UserDB
from .....crud import transaction
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
                                pagination_params: PaginationParams = Depends(),
                                date_filters: DateFilters = Depends(),
                                type_filters: TransactionTypeFilters = Depends(),
                                sort_by: TransactionSortBy = Depends(),
                                db: Session = Depends(get_db)):

    transactions, total_transactions = transaction.get_multi_by_owner(
        db=db,
        user_id=user.id,
        **pagination_params.dict(),
        **date_filters.dict(),
        **type_filters.dict(),
        **sort_by.dict(),
        get_total=True
    )

    return PaginatedTransaction(
        transactions=transactions,
        total_transactions=total_transactions
    )


@router.get("/{id}", response_model=TransactionOut)
async def get_user_transaction(id: int,
                               user: UserDB = Depends(fastapi_users.get_current_active_user),
                               db: Session = Depends(get_db)):

    existing_transaction = transaction.get_by_owner(db=db, id=id, user_id=user.id)
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return existing_transaction


@router.post('', response_model=TransactionOut)
async def create_transaction(transaction_in: TransactionCreate,
                             user: UserDB = Depends(fastapi_users.get_current_active_user),
                             db: Session = Depends(get_db)):

    new_transaction = transaction.create_with_owner(
        db=db,
        obj_in=transaction_in,
        user_id=user.id
    )

    return new_transaction


@router.put("/{id}", response_model=TransactionOut)
async def update_transaction(id: int,
                             transaction_in: TransactionUpdate,
                             user: UserDB = Depends(fastapi_users.get_current_active_user),
                             db: Session = Depends(get_db)):

    existing_transaction = transaction.get_by_owner(db=db, id=id, user_id=user.id)
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    updated_transaction = transaction.update(
        db=db,
        db_obj=existing_transaction,
        obj_in=transaction_in
    )

    return updated_transaction


@router.delete("/{id}", response_model=TransactionOut)
async def delete_transaction(id: int,
                             user: UserDB = Depends(fastapi_users.get_current_active_user),
                             db: Session = Depends(get_db)):

    existing_transaction = transaction.get_by_owner(db=db, id=id, user_id=user.id)
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    removed_transaction = transaction.remove(db=db, id=id)
    return removed_transaction


@router.post('/import/legacy', response_model=List[TransactionOut])
async def import_data(transactions_in: List[LegacyTransaction],
                      user: UserDB = Depends(fastapi_users.get_current_active_user),
                      db: Session = Depends(get_db)):

    new_transactions = []
    for tx in transactions_in:
        price = tx.price if tx.incoming else -tx.price
        new_transaction = transaction.create_with_owner(
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
