import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(), default=datetime.datetime.utcnow)
    price = Column(Float())
    comment = Column(String(500))
    type = Column(String(50))

    def __str__(self):
        return "(date: %s, price: %f, type: %s, comment: %s)" % (
            "test",
            self.price,
            self.type,
            self.comment,
        )
