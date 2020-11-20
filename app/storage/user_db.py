from databases import Database

from .schemas.users import UserDB
from ..settings import settings
from ..fastapi_users import SQLAlchemyUserDatabase
from .models import UserTable, OAuthAccount

users = UserTable.__table__
oauth_accounts = OAuthAccount.__table__

database = Database(settings.DATABASE_URL)
user_db = SQLAlchemyUserDatabase(UserDB, database, users, oauth_accounts)