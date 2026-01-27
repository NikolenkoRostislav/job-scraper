from fastapi import APIRouter, Request, Cookie, Depends, Body
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas import Token, Tokens
from src.services import AuthService, EmailService
from src.api.dependencies import DatabaseDep, CurrentUserDep
from src.api.exception_handler import handle_exceptions
from src.utils.oauth import oauth
from src.utils.classes import UnauthorizedError
from src.config import settings


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Tokens)
@handle_exceptions
async def get_token(db: DatabaseDep, form_data: OAuth2PasswordRequestForm = Depends()):
    tokens = await AuthService.login(form_data.username, form_data.password, db)

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
    
    access_token = await AuthService.refresh_token(refresh_token, db)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request, db: DatabaseDep):
    # Only the refresh token cookie can be returned so frontend must call /auth/refresh to get the access token
    refresh_token = await AuthService.login_with_google(request, db)

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
async def send_email_code(receiver: str = Body()):
    #return await EmailService.send_email_code(receiver)
    return "I havent actually implemented this yet"