from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    skip: int = Query(0, title="skip the first x results", ge=0)
    limit: int = Query(100, title="skip the first x results", ge=1)