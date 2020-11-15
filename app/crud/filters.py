from datetime import datetime
from typing import List
from abc import ABC, abstractmethod
import pendulum
from sqlalchemy.sql.expression import BinaryExpression
from .base import ModelType


class Filter(ABC):
    def __init__(self, model: ModelType, filter_func):
        self._model = model
        self._filter_func = filter_func

    @abstractmethod
    def __call__(self):
        raise NotImplementedError()


class MonthFilter(Filter):
    def __init__(self, model: ModelType, column_name: str, month: int = None, year: int = None):
        super().__init__(model, filter_in_month)
        self._column_name = column_name
        self._month = month
        self._year = year

    def __call__(self):
        return self._filter_func(
            model=self._model,
            column_name=self._column_name,
            month=self._month,
            year=self._year
        )
        
class DateFilter(Filter):
    def __init__(self, model: ModelType, column_name: str, start: datetime = None, end: datetime = None):
        super().__init__(model, filter_in_date_range)
        self._column_name = column_name
        self._start = start
        self._end = end

    def __call__(self):
        return self._filter_func(
            model=self._model,
            column_name=self._column_name,
            start=self._start,
            end=self._end
        )

def filter_in_date_range(model: ModelType, column_name, start: datetime, end: datetime) -> List[BinaryExpression]:

    if start is None and end is None:
        return []
    
    if start is None:
        start = pendulum.datetime(1900, 1, 1)
        
    if end is None:
        end = pendulum.datetime(3000, 12, 31).end_of("day")

    model_operand = getattr(model, column_name, None)
    if not model_operand:
        raise AttributeError()

    return [
        model_operand >= start,
        model_operand <= end
    ]


def filter_in_month(model: ModelType, column_name, month: int, year: int) -> List[BinaryExpression]:

    if year is None:
        return []

    if month is None:
        begin = pendulum.datetime(year, 1, 1)
        end = begin.last_of("year").end_of("day")
    else:
        begin = pendulum.datetime(year, month, 1)
        end = begin.last_of("month").end_of("day")

    model_operand = getattr(model, column_name, None)
    if not model_operand:
        raise AttributeError()

    return [
        model_operand >= begin,
        model_operand <= end
    ]
