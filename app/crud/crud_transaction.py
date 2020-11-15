from typing import List

from fastapi.encoders import jsonable_encoder
from pydantic import UUID4 as GUID
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..storage.models import TransactionTable as Transaction
from ..storage.schemas.transactions import TransactionCreate, TransactionUpdate


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: TransactionCreate, user_id: GUID
    ) -> Transaction:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_owner(
        self, db: Session, *, id: int, user_id: GUID
    ) -> List[Transaction]:
        return (
            db.query(self.model)
            .filter(Transaction.user_id == user_id,
                    Transaction.id == id)
            .one_or_none()
        )
        

    def get_multi_by_owner(
        self, db: Session, *, user_id: GUID, skip: int = 0, limit: int = 100
    ) -> List[Transaction]:
        return (
            db.query(self.model)
            .filter(Transaction.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


transaction = CRUDTransaction(Transaction)
