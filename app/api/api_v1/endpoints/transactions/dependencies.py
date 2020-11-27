from app.crud.filters import DateFilter
from datetime import datetime
from enum import Enum
from typing import Any, Callable, List, Optional, Tuple, Union
from databases.core import Transaction
from fastapi import Query
from pydantic import BaseModel
from app.utils import rgetattr


# class DateFilters(BaseModel):
#     year: Optional[int] = Query(
#         None,
#         description="The year of the month to get the stats from",
#         ge=1900,
#         le=3000
#     )
#     month: Optional[int] = Query(
#         None,
#         description="The month numerically to get the stats from",
#         ge=1,
#         le=12
#     )
#     start_date: Optional[datetime] = Query(
#         None,
#         description="Start Date"
#     )
#     end_date: Optional[datetime] = Query(
#         None,
#         description="End date"
#     )

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
