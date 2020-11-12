from typing import Mapping
from fastapi_users.models import UD
from fastapi_users.db import SQLAlchemyUserDatabase


async def _make_user(self, user: Mapping) -> UD:
    user_dict = {**user}

    if self.oauth_accounts is not None:
        query = self.oauth_accounts.select().where(
            self.oauth_accounts.c.user_id == user["id"]
        )
        oauth_accounts = await self.database.fetch_all(query)
        # PATCHING THIS DUE PENDATIC VALIDATION ERROR
        # user_dict["oauth_accounts"] = oauth_accounts
        user_dict["oauth_accounts"] = [{**account}
                                       for account in oauth_accounts]

    return self.user_db_model(**user_dict)


SQLAlchemyUserDatabase._make_user = _make_user
