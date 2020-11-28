from enum import Enum
from typing import TypeVar, Type, Optional
from fastapi import Query

from app.crud.base import ModelType


# class PaginationParams(BaseModel):
#     skip: int = Query(0, title="skip the first x results", ge=0)
#     limit: int = Query(100, title="skip the first x results", ge=1)

EnumType = TypeVar("EnumType", bound=Enum)


def model_enum(model: Type[ModelType]) -> Type[EnumType]:
    _enum_content = {key: key for key in model.__table__.columns.keys()}
    return Enum(f"{model.__class__.__name__}Enum", _enum_content)


class SortBy:

    def __init__(self,
                 sort_by: Optional[EnumType] = Query(None, description="sort by"),
                 descending_order: Optional[bool] = Query(None, description="descending order")) -> None:
        self.sort_by = sort_by
        self.descending_order = descending_order if descending_order is not None else False

    def dict(self):
        return dict(order_attribute=getattr(self.sort_by, 'value', None),
                    desc_order=self.descending_order)


class PaginationParams:
    def __init__(self,
                 skip: int = Query(0, description="Skip the first x results", ge=0),
                 limit: int = Query(100, description="Skip the first x results", ge=1)
                 ):
        self.skip = skip
        self.limit = limit

    def dict(self):
        return dict(skip=self.skip, limit=self.limit)