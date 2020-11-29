from fastapi import APIRouter
from httpx_oauth.clients.google import GoogleOAuth2
from fastapi_utils.inferring_router import InferringRouter

from ...settings import settings
from ...background_tasks import on_after_register, on_after_forgot_password
from ...fastapi_users import fastapi_users, jwt_authentication

google_oauth_client = GoogleOAuth2(
    settings.GOOGLE_OAUTH_CLIENT_ID,
    settings.GOOGLE_OAUTH_CLIENT_SECRET
)

api_router = InferringRouter()
google_oauth_router = fastapi_users.get_oauth_router(
    google_oauth_client, settings.SECRET, after_register=on_after_register
)
api_router.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"]
)
api_router.include_router(
    fastapi_users.get_register_router(on_after_register),
    prefix="/auth",
    tags=["auth"]
)
api_router.include_router(
    fastapi_users.get_reset_password_router(
        settings.SECRET,
        after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"]
)
api_router.include_router(
    google_oauth_router,
    prefix="/auth/google",
    tags=["auth"]
)
