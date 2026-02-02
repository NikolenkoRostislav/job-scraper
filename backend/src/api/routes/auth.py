from fastapi import APIRouter, Request, Cookie, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.core.oauth import oauth
from src.core.config import settings
from src.api.dependencies import DatabaseDep, rate_limit_token
from src.api.exception_handler import handle_exceptions
from src.services import AuthService, EmailService
from src.schemas import Token, Tokens, Email
from src.utils import UnauthorizedError


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Tokens, dependencies=[Depends(rate_limit_token)])
@handle_exceptions
async def get_token(db: DatabaseDep, form_data: OAuth2PasswordRequestForm = Depends()):
    tokens = await AuthService.login(db, form_data.username, form_data.password)

    response = JSONResponse(
        content={
            "access_token": tokens["access_token"],
            "token_type": "bearer"
        }
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS*24*60*60  
    )

    return response


@router.post("/refresh", response_model=Token)
@handle_exceptions
async def refresh_token(db: DatabaseDep, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise UnauthorizedError("Missing refresh token")
    
    access_token = await AuthService.refresh_token(db, refresh_token)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/google/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(request, settings.GOOGLE_CALLBACK_URL)


@router.get("/google/callback")
async def google_callback(db: DatabaseDep, request: Request):
    # Only the refresh token cookie can be returned so frontend must call /auth/refresh to get the access token
    refresh_token = await AuthService.login_with_google(db, request)

    response = RedirectResponse(settings.FRONTEND_REDIRECT_URL)
   
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS*24*60*60  
    )

    return response


@router.post("/send/email-code")
@handle_exceptions
async def send_email_code(db: DatabaseDep, receiver: Email):
    return await EmailService.send_email_code(db, receiver)
