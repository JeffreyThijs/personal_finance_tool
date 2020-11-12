from httpx_oauth.clients.google import GoogleOAuth2
from .settings import settings

google_oauth_client = GoogleOAuth2(
    settings.GOOGLE_OAUTH_CLIENT_ID,
    settings.GOOGLE_OAUTH_CLIENT_SECRET
)
