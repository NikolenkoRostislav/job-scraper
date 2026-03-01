from fastapi import APIRouter, Request, Cookie, Depends, BackgroundTasks
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from core.oauth import oauth
from core.config import settings
from api.dependencies import DatabaseDep
from api.rate_limiter import rate_limit_token_by_username, rate_limit_token_by_ip
from shared.services import AuthService, EmailService
from shared.schemas import Token, Tokens
from shared.utils import PermissionDeniedError


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Tokens, dependencies=[Depends(rate_limit_token_by_username), Depends(rate_limit_token_by_ip)])
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
        secure=not settings.app.DEBUG,
        samesite="lax",
        max_age=settings.auth.REFRESH_TOKEN_EXPIRE_DAYS*24*60*60  
    )

    return response


@router.post("/refresh", response_model=Token)
async def refresh_token(db: DatabaseDep, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise PermissionDeniedError("Missing refresh token")
    
    access_token = await AuthService.refresh_token(db, refresh_token)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/google/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(request, settings.auth.GOOGLE_CALLBACK_URL)


@router.get("/google/callback")
async def google_callback(db: DatabaseDep, request: Request):
    # Only the refresh token cookie can be returned so frontend must call /auth/refresh to get the access token
    refresh_token = await AuthService.login_with_google(db, request)

    response = RedirectResponse(settings.auth.FRONTEND_REDIRECT_URL)
   
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.app.DEBUG,
        samesite="lax",
        max_age=settings.auth.REFRESH_TOKEN_EXPIRE_DAYS*24*60*60  
    )

    return response


@router.post("/send/email-code")
async def send_email_code(db: DatabaseDep, background_tasks: BackgroundTasks, receiver: EmailStr):
    code = await EmailService.create_email_code(db, receiver)
    background_tasks.add_task(EmailService.send_email_code, receiver, code)
    return {"message": "sending email"}


@router.delete("/logout")
async def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie(key="refresh_token")
    return response
