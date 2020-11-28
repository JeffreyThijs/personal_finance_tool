from app.storage.models import TransactionTable
from app.crud.base import ModelType
from datetime import datetime
from enum import Enum
from typing import Any, Callable, List, Optional, Tuple, Type, TypeVar
from fastapi import Query
from app.utils import rgetattr
from ..dependencies import SortBy, model_enum


def group_by_func(model, attrs: List[str]) -> Tuple[Any, ...]:
    return tuple([rgetattr(model, attr) for attr in attrs])


def group_by_month_func(model) -> Callable:
    return group_by_func(model, ['date.year', 'date.month'])


class PartitionFunction(str, Enum):
    by_month = 'by_month'

    @property
    def func(self):
        return FUNC_MAPPING[self]

    @property
    def order_attribute(self) -> str:
        if self.value == self.by_month.value:
            return 'date'
        else:
            raise NotImplementedError()


FUNC_MAPPING = {
    PartitionFunction.by_month: group_by_month_func
}


class DateFilters:
    def __init__(self,
                 year: Optional[int] = Query(
                     None, description="The year of the month you want to filter on", ge=1900, le=3000),
                 month: Optional[int] = Query(
                     None, description="The month numerically to filter on", ge=1, le=12),
                 start_date: Optional[datetime] = Query(None, description="Start date to filter on"),
                 end_date: Optional[datetime] = Query(None, description="End date to filter on")
                 ):
        self.year = year
        self.month = month
        self.start_date = start_date
        self.end_date = end_date

    def dict(self):
        return dict(
            year=self.year,
            month=self.month,
            start_date=self.start_date,
            end_date=self.end_date
        )


class TransactionTypeFilters:
    def __init__(self,
                 incoming: bool = Query(
                     None, description="Wether to filter on incoming"),
                 ):
        self.incoming = incoming

    def dict(self):
        return dict(
            incoming=self.incoming
        )


class TransactionSortBy(SortBy):

    def __init__(self,
                 sort_by: Optional[model_enum(TransactionTable)] = Query(None, description="sort by"),
                 descending_order: Optional[bool] = Query(None, description="descending order")) -> None:
        super().__init__(sort_by, descending_order)


class PartitionalDateFilters(DateFilters):

    def __init__(self,
                 year: Optional[int] = Query(
                     None, description="The year of the month you want to filter on", ge=1900, le=3000),
                 month: Optional[int] = Query(
                     None, description="The month numerically to filter on", ge=1, le=12),
                 start_date: Optional[datetime] = Query(None, description="Start date to filter on"),
                 end_date: Optional[datetime] = Query(None, description="End date to filter on"),
                 partition_by: Optional[PartitionFunction] = Query(None, description="partition the results by")
                 ) -> None:
        super().__init__(year=year, month=month, start_date=start_date, end_date=end_date)
        self.order_attribute = getattr(partition_by, 'order_attribute', None)
        self.partition_func = partition_by

    def dict(self):
        return dict(
            year=self.year,
            month=self.month,
            start_date=self.start_date,
            end_date=self.end_date,
            order_attribute=self.order_attribute,
            partition_func=getattr(self.partition_func, 'func', None)
        )
