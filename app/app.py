from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from httpx_oauth.clients.google import GoogleOAuth2

from .config import Config
from .post_request_methods import on_after_register, on_after_forgot_password
from .storage.models import database, user_db
from .storage.schemas import User, UserCreate, UserUpdate, UserDB

config = Config.from_environ()

jwt_authentication = JWTAuthentication(
    secret=config.SECRET, 
    lifetime_seconds=3600, 
    tokenUrl="/auth/jwt/login"
)

google_oauth_client = GoogleOAuth2(
    config.GOOGLE_OAUTH_CLIENT_ID,
    config.GOOGLE_OAUTH_CLIENT_SECRET
)

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=config.DATABASE_URL)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(
        config.SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(),
                   prefix="/users", tags=["users"])

google_oauth_router = fastapi_users.get_oauth_router(
    google_oauth_client, config.SECRET, after_register=on_after_register
)
app.include_router(google_oauth_router, prefix="/auth/google", tags=["auth"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
