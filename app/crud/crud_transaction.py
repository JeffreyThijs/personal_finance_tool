import operator
from datetime import datetime
import operator
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import UUID4 as GUID
from sqlalchemy import desc
from sqlalchemy.orm import Session

from .base import CRUDBase
from .filters import ConditionFilter, DateFilter, MonthFilter
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
        self,
        db: Session,
        *,
        id: int,
        user_id: GUID,
        month: int = None,
        year: int = None,
        start: datetime = None,
        end: datetime = None,
        incoming: bool = None,
        order_attribute: str = None,
        desc_order: bool = False
    ) -> List[Transaction]:

        filters = [
            *MonthFilter(self.model, "date", month, year)(),
            *DateFilter(self.model, "date", start, end)()
        ]
        
        if incoming is not None:
            op = operator.ge if incoming else operator.lt
            filters.extend(
                ConditionFilter(self.model, "price", op, 0.0)()
            )

        return (
            db.query(self.model)
            .filter(Transaction.user_id == user_id,
                    Transaction.id == id,
                    *filters)
            .one_or_none()
        )

    def get_multi_by_owner(
        self,
        db: Session,
        *,
        user_id: GUID,
        skip: int = 0,
        limit: int = 100,
        month: int = None,
        year: int = None,
        start_date: datetime = None,
        end_date: datetime = None,
        incoming: bool = None,
        order_attribute: str = None,
        desc_order: bool = False
    ) -> List[Transaction]:

        filters = [
            *MonthFilter(self.model, "date", month, year)(),
            *DateFilter(self.model, "date", start_date, end_date)()
        ]
        
        if incoming is not None:
            op = operator.ge if incoming else operator.lt
            filters.extend(
                ConditionFilter(self.model, "price", op, 0.0)()
            )

        transaction_q = db.query(self.model)\
                          .filter(Transaction.user_id == user_id, *filters)

        if skip is not None:
            transaction_q = transaction_q.offset(skip)
        if limit is not None:
            transaction_q = transaction_q.limit(limit)
            
            
        if order_attribute is not None:
            if sort_obj := getattr(self.model, order_attribute, None):
                if desc_order:
                    sort_obj = desc(sort_obj)
                transaction_q = transaction_q.order_by(sort_obj)
            
        return transaction_q.all()


transaction = CRUDTransaction(Transaction)
