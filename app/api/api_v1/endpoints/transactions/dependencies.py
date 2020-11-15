from datetime import datetime
from typing import Optional
from fastapi import Query
from pydantic import BaseModel


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
