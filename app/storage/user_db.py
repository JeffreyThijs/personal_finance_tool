from databases import Database

from .schemas.users import UserDB
from .models import UserTable, OAuthAccount
from ..fastapi_users.sa_user_db import SQLAlchemyUserDatabase
from ..settings import get_settings

users = UserTable.__table__
oauth_accounts = OAuthAccount.__table__

settings = get_settings()
database = Database(settings.DATABASE_URL,
                    min_size=settings.MIN_DB_SESSIONS,
                    max_size=settings.MAX_DB_SESSIONS)
user_db = SQLAlchemyUserDatabase(UserDB, database, users, oauth_accounts)
