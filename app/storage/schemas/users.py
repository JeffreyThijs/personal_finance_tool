from typing import Optional
from fastapi_users import models
from pydantic.types import constr


class User(models.BaseUser, models.BaseOAuthAccountMixin):
    pass


class UserCreate(models.BaseUserCreate):
    password: constr(min_length=8)


class UserUpdate(User, models.BaseUserUpdate):
    password: Optional[constr(min_length=8)]


class UserDB(User, models.BaseUserDB):
    pass