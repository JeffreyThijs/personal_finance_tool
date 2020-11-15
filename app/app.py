from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from .settings import settings
from .background_tasks import on_after_register, on_after_forgot_password
from .storage.models import database
from .endpoints import transactions
from .users import fastapi_users, jwt_authentication
from .oauth import google_oauth_client


app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://127.0.0.1",
    "http://localhost:8080"
]

app.add_middleware(
CORSMiddleware,
    allow_origins=origins, # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)


app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(
        settings.SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(),
                   prefix="/users", tags=["users"])

google_oauth_router = fastapi_users.get_oauth_router(
    google_oauth_client, settings.SECRET, after_register=on_after_register
)
app.include_router(google_oauth_router, prefix="/auth/google", tags=["auth"])

app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
