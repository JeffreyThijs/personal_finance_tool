import jwt
import urllib.parse as urlparse
from urllib.parse import urlencode
from typing import Callable, Mapping, List, Optional, Type, cast, Any

from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import BaseOAuth2

from fastapi_users.models import BaseUserDB
from fastapi_users import FastAPIUsers
from fastapi_users.router.oauth import generate_state_token, decode_state_token
from fastapi_users import models
from fastapi_users.authentication import Authenticator, BaseAuthentication
from fastapi_users.db import BaseUserDatabase
from fastapi_users.password import generate_password, get_password_hash
from fastapi_users.router.common import ErrorCode, run_handler
from fastapi_users.authentication.cookie import CookieAuthentication
from fastapi_users.authentication.jwt import JWTAuthentication

from ..storage.schemas.users import User, UserCreate, UserUpdate, UserDB
from ..storage.user_db import user_db
from ..settings import settings



async def get_login_redirected_response(self, user: BaseUserDB, response: Response, redirect_uri: str) -> Any:
    raise NotImplementedError()

BaseAuthentication.get_login_redirected_response = get_login_redirected_response


async def get_login_redirected_response_cookie(self, user: BaseUserDB, response: Response, redirect_uri: str) -> Any:
    token = await self._generate_token(user)
    response.set_cookie(
        self.cookie_name,
        token,
        max_age=self.lifetime_seconds,
        path=self.cookie_path,
        domain=self.cookie_domain,
        secure=self.cookie_secure,
        httponly=self.cookie_httponly,
        samesite=self.cookie_samesite,
    )

    return RedirectResponse(redirect_uri)

CookieAuthentication.get_login_redirected_response = get_login_redirected_response_cookie


def _generate_redirect_url(base_url: str, options: dict) -> str:

    url_parts = list(urlparse.urlparse(base_url))

    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(options)

    url_parts[4] = urlencode(query)

    return urlparse.urlunparse(url_parts)


async def get_login_redirected_response_jwt(self, user: BaseUserDB, response: Response, redirect_uri: str) -> Any:
    token = await self._generate_token(user)

    return RedirectResponse(
        _generate_redirect_url(
            base_url=redirect_uri,
            options={"access_token": token, "token_type": "bearer"}
        )
    )

JWTAuthentication.get_login_redirected_response = get_login_redirected_response_jwt


def _get_oauth_router(
    oauth_client: BaseOAuth2,
    user_db: BaseUserDatabase[models.BaseUserDB],
    user_db_model: Type[models.BaseUserDB],
    authenticator: Authenticator,
    state_secret: str,
    redirect_url: str = None,
    after_register: Optional[Callable[[models.UD, Request], None]] = None,
) -> APIRouter:
    """Generate a router with the OAuth routes."""
    router = APIRouter()
    callback_route_name = f"{oauth_client.name}-callback"

    if redirect_url is not None:
        oauth2_authorize_callback = OAuth2AuthorizeCallback(
            oauth_client,
            redirect_url=redirect_url,
        )
    else:
        oauth2_authorize_callback = OAuth2AuthorizeCallback(
            oauth_client,
            route_name=callback_route_name,
        )

    @router.get("/authorize")
    async def authorize(
        request: Request,
        authentication_backend: str,
        scopes: List[str] = Query(None),
        redirect_uri: Optional[str] = None
    ):
        # Check that authentication_backend exists
        backend_exists = False
        for backend in authenticator.backends:
            if backend.name == authentication_backend:
                backend_exists = True
                break
        if not backend_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if redirect_url is not None:
            authorize_redirect_url = redirect_url
        else:
            authorize_redirect_url = request.url_for(callback_route_name)

        state_data = {
            "authentication_backend": authentication_backend,
            "post_callback_redirect_uri": redirect_uri
        }
        state = generate_state_token(state_data, state_secret)
        authorization_url = await oauth_client.get_authorization_url(
            authorize_redirect_url,
            state,
            scopes,
        )

        return {"authorization_url": authorization_url}

    @router.get("/callback", name=f"{oauth_client.name}-callback")
    async def callback(
        request: Request,
        response: Response,
        access_token_state=Depends(oauth2_authorize_callback),
    ):
        token, state = access_token_state
        account_id, account_email = await oauth_client.get_id_email(
            token["access_token"]
        )

        try:
            state_data = decode_state_token(state, state_secret)
        except jwt.DecodeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        user = await user_db.get_by_oauth_account(oauth_client.name, account_id)

        new_oauth_account = models.BaseOAuthAccount(
            oauth_name=oauth_client.name,
            access_token=token["access_token"],
            expires_at=token["expires_at"],
            refresh_token=token.get("refresh_token"),
            account_id=account_id,
            account_email=account_email,
        )

        if not user:
            user = await user_db.get_by_email(account_email)
            if user:
                # Link account
                user.oauth_accounts.append(new_oauth_account)  # type: ignore
                await user_db.update(user)
            else:
                # Create account
                password = generate_password()
                user = user_db_model(
                    email=account_email,
                    hashed_password=get_password_hash(password),
                    oauth_accounts=[new_oauth_account],
                )
                await user_db.create(user)
                if after_register:
                    await run_handler(after_register, user, request)
        else:
            # Update oauth
            updated_oauth_accounts = []
            for oauth_account in user.oauth_accounts:  # type: ignore
                if oauth_account.account_id == account_id:
                    updated_oauth_accounts.append(new_oauth_account)
                else:
                    updated_oauth_accounts.append(oauth_account)
            user.oauth_accounts = updated_oauth_accounts  # type: ignore
            await user_db.update(user)

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )

        # Authenticate
        for backend in authenticator.backends:
            if backend.name == state_data["authentication_backend"]:
                redirect_uri = state_data.get(
                    "post_callback_redirect_uri", None)
                if redirect_uri is not None:
                    return await backend.get_login_redirected_response(
                        cast(models.BaseUserDB, user), response, redirect_uri
                    )
                else:
                    return await backend.get_login_response(
                        cast(models.BaseUserDB, user), response
                    )

    return router


def get_oauth_router(
    self,
    oauth_client: BaseOAuth2,
    state_secret: str,
    redirect_url: str = None,
    after_register: Optional[Callable[[models.UD, Request], None]] = None,
) -> APIRouter:
    """
    Return an OAuth router for a given OAuth client.

    :param oauth_client: The HTTPX OAuth client instance.
    :param state_secret: Secret used to encode the state JWT.
    :param redirect_url: Optional arbitrary redirect URL for the OAuth2 flow.
    If not given, the URL to the callback endpoint will be generated.
    :param after_register: Optional function called
    after a successful registration.
    """
    return _get_oauth_router(
        oauth_client,
        self.db,
        self._user_db_model,
        self.authenticator,
        state_secret,
        redirect_url,
        after_register,
    )


FastAPIUsers.get_oauth_router = get_oauth_router


jwt_authentication = JWTAuthentication(
    secret=settings.SECRET,
    lifetime_seconds=3600,
    tokenUrl="/auth/jwt/login"
)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
