import operator
from sqlalchemy import and_, or_
from app.api.api_v1.endpoints.transactions.dependencies import PartitionFunction, TagCondition
from itertools import groupby
from datetime import datetime
from typing import Any, Iterable, List, Tuple, Union

from pydantic import UUID4 as GUID
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from .filters import ConditionFilter, DateFilter, MonthFilter
from ..storage.models import TransactionTable as Transaction
from ..storage.schemas.transactions import TransactionCreate, TransactionUpdate

TXS = List[Transaction]


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: TransactionCreate, user_id: GUID
    ) -> Transaction:
        obj_in_data = self._encode(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def get_by_owner(
        self,
        db: AsyncSession,
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
    ) -> TXS:

        filters = [
            *MonthFilter(self.model, "date", month, year)(),
            *DateFilter(self.model, "date", start, end)()
        ]

        if incoming is not None:
            op = operator.ge if incoming else operator.lt
            filters.extend(
                ConditionFilter(self.model, "price", op, 0.0)()
            )

        stmt = select(self.model).filter(
            Transaction.user_id == user_id,
            Transaction.id == id,
            *filters
        )

        db_execute = await db.execute(stmt)
        return db_execute.scalars().one_or_none()

    async def get_multi_by_owner(
        self,
        db: AsyncSession,
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
        desc_order: bool = False,
        get_total: bool = False,
        partition_func: PartitionFunction = None,
        tags: List[str] = None,
        tag_condition: TagCondition = None
    ) -> Union[TXS, Tuple[TXS, int], Iterable[Tuple[Any, Iterable[TXS]]], Tuple[Iterable[Tuple[Any, Iterable[TXS]]], int]]:

        filters = [
            *MonthFilter(self.model, "date", month, year)(),
            *DateFilter(self.model, "date", start_date, end_date)()
        ]

        if incoming is not None:
            op = operator.ge if incoming else operator.lt
            filters.extend(
                ConditionFilter(self.model, "price", op, 0.0)()
            )

        stmt = select(self.model).filter(
            Transaction.user_id == user_id,
            *filters
        )

        if tags is not None and tag_condition is not None:
            if tag_condition is TagCondition.any:
                tag_filters = [Transaction.tags.any(tag) for tag in tags]
                tag_filters = or_(*tag_filters)
            elif tag_condition is TagCondition.all:
                tag_filters = [Transaction.tags.any(tag) for tag in tags]
                tag_filters = and_(*tag_filters)
            else:
                raise NotImplementedError("unknown condition")

            stmt = stmt.filter(tag_filters)

        if order_attribute is not None:
            if sort_obj := getattr(self.model, order_attribute, None):
                if desc_order:
                    sort_obj = desc(sort_obj)
                stmt = stmt.order_by(sort_obj)

        count_stmt = stmt

        if skip is not None:
            stmt = stmt.offset(skip)
        if limit is not None:
            stmt = stmt.limit(limit)

        db_execute = await db.execute(stmt)
        found_transactions = db_execute.scalars().all()

        if partition_func is not None:
            found_transactions = groupby(found_transactions, partition_func)

        if get_total:
            db_execute = await db.execute(count_stmt)
            return (found_transactions, len(db_execute.scalars().all()))

        return found_transactions


transaction = CRUDTransaction(Transaction)
