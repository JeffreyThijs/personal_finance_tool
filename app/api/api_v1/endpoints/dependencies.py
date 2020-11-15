from fastapi import Query
from pydantic import BaseModel


# class PaginationParams(BaseModel):
#     skip: int = Query(0, title="skip the first x results", ge=0)
#     limit: int = Query(100, title="skip the first x results", ge=1)

class PaginationParams:
    def __init__(self,
                 skip: int = Query(0, description="Skip the first x results", ge=0),
                 limit: int = Query(100, description="Skip the first x results", ge=1)
                 ):
        self.skip = skip
        self.limit = limit
        
    def dict(self):
        return dict(skip=self.skip, limit=self.limit)
