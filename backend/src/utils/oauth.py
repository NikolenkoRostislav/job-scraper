from authlib.integrations.starlette_client import OAuth
from fastapi.security import OAuth2PasswordBearer

from src.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
