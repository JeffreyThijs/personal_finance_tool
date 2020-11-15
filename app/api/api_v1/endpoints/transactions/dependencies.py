from datetime import datetime
from typing import Optional
from fastapi import Query
from pydantic import BaseModel


class DateFilters(BaseModel):
    year: Optional[int] = Query(None, title="The year of the month to get the stats from", ge=1900, le=3000)
    month: Optional[int] = Query(None, title="The month numerically to get the stats from", ge=1, le=12)
    start_date: Optional[datetime] = Query(None, title="start date")
    end_date: Optional[datetime] = Query(None, title="end date")
