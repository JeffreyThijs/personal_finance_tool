from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.param_functions import Query
from fastapi_sqlalchemy import db
from app.fastapi_users import fastapi_users

from .statistics import router as stats_router
from .....storage.schemas.users import UserDB
from .....crud import transaction
from .....storage.schemas.transactions import TransactionOut, TransactionCreate, TransactionUpdate

router = APIRouter()


@router.get('/', response_model=List[TransactionOut])
def get_user_transactions(user: UserDB = Depends(fastapi_users.get_current_active_user),
                          skip: int = 0,
                          limit: int = 100,
                          year: int = Query(None, title="The year of the month to get the stats from", ge=1900, le=3000), 
                          month: int = Query(None, title="The month numerically to get the stats from", ge=1, le=12)):

    transactions = transaction.get_multi_by_owner(
        db=db.session,
        user_id=user.id,
        skip=skip,
        limit=limit,
        month=month,
        year=year
    )

    return transactions

@router.get("/{id}", response_model=TransactionOut)
def get_user_transaction(id: int,
                         user: UserDB = Depends(fastapi_users.get_current_active_user)):

    existing_transaction = transaction.get_by_owner(db=db.session, id=id, user_id=user.id)
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return existing_transaction


@router.post('/', response_model=TransactionOut)
def create_transaction(transaction_in: TransactionCreate,
                       user: UserDB = Depends(fastapi_users.get_current_active_user)):

    new_transaction = transaction.create_with_owner(
        db=db.session,
        obj_in=transaction_in,
        user_id=user.id
    )

    return new_transaction


@router.put("/{id}", response_model=TransactionOut)
def update_transaction(id: int,
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
def delete_transaction(id: int,
                       user: UserDB = Depends(fastapi_users.get_current_active_user)):

    existing_transaction = transaction.get_by_owner(db=db.session, id=id, user_id=user.id)
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    removed_transaction = transaction.remove(db=db.session, id=id)
    return removed_transaction


router.include_router(stats_router, prefix="/stats", tags=["statistics"])
