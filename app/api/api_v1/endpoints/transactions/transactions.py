from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from app.fastapi_users import fastapi_users

from .statistics import router as stats_router
from .dependencies import DateFilters
from ..dependencies import PaginationParams
from .....storage.schemas.users import UserDB
from .....crud import transaction
from .....storage.schemas.transactions import TransactionOut, TransactionCreate, TransactionUpdate

router = APIRouter()
router.include_router(stats_router, prefix="/stats", tags=["statistics"])


@router.get('', response_model=List[TransactionOut])
async def get_user_transactions(user: UserDB = Depends(fastapi_users.get_current_active_user),
                                pagination_params: PaginationParams = Depends(),
                                date_filters: DateFilters = Depends()):

    transactions = transaction.get_multi_by_owner(
        db=db.session,
        user_id=user.id,
        **pagination_params.dict(),
        **date_filters.dict()
    )

    return transactions


@router.get("/{id}", response_model=TransactionOut)
async def get_user_transaction(id: int,
                               user: UserDB = Depends(fastapi_users.get_current_active_user)):

    existing_transaction = transaction.get_by_owner(db=db.session, id=id, user_id=user.id)
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return existing_transaction


@router.post('', response_model=TransactionOut)
async def create_transaction(transaction_in: TransactionCreate,
                             user: UserDB = Depends(fastapi_users.get_current_active_user)):

    new_transaction = transaction.create_with_owner(
        db=db.session,
        obj_in=transaction_in,
        user_id=user.id
    )

    return new_transaction


@router.put("/{id}", response_model=TransactionOut)
async def update_transaction(id: int,
                             transaction_in: TransactionUpdate,
                             user: UserDB = Depends(fastapi_users.get_current_active_user)):

    existing_transaction = transaction.get_by_owner(db=db.session, id=id, user_id=user.id)
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    updated_transaction = transaction.update(
        db=db.session,
        db_obj=existing_transaction,
        obj_in=transaction_in
    )

    return updated_transaction


@router.delete("/{id}", response_model=TransactionOut)
async def delete_transaction(id: int,
                             user: UserDB = Depends(fastapi_users.get_current_active_user)):

    existing_transaction = transaction.get_by_owner(db=db.session, id=id, user_id=user.id)
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    removed_transaction = transaction.remove(db=db.session, id=id)
    return removed_transaction
