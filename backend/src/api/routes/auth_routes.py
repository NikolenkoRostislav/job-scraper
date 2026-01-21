from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.api.schemas import Token, RefreshTokenRequest, Tokens
from src.services import AuthService
from src.api.dependancies import DatabaseDep
from src.api.exception_handler import handle_exceptions


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Tokens)
@handle_exceptions
async def get_token(db: DatabaseDep, form_data: OAuth2PasswordRequestForm = Depends()):
    tokens = await AuthService.login(form_data.username, form_data.password, db)

    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
@handle_exceptions
async def refresh_token(db: DatabaseDep, token_data: RefreshTokenRequest):
    access_token = await AuthService.refresh_token(token_data.refresh_token, db)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
