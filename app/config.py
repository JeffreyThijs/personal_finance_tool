from __future__ import annotations

import os
from re import L
from dotenv import load_dotenv

from pydantic import BaseModel


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config(BaseModel):
    SECRET: str
    DATABASE_URL: str
    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str
    
    @classmethod
    def from_environ(cls) -> Config:
        return cls(
            SECRET=os.environ["SECRET"],
            DATABASE_URL=os.environ["DATABASE_URL"],
            GOOGLE_OAUTH_CLIENT_ID=os.environ["GOOGLE_OAUTH_CLIENT_ID"],
            GOOGLE_OAUTH_CLIENT_SECRET=os.environ["GOOGLE_OAUTH_CLIENT_SECRET"]
        )