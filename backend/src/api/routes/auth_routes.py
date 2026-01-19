from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.api.schemas import Token
from src.api.auth_service import AuthService
from src.db.session import DatabaseDep
from src.api.exception_handler import handle_exceptions


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
@handle_exceptions
async def login(db: DatabaseDep, form_data: OAuth2PasswordRequestForm = Depends()):
    tokens = await AuthService.login(form_data.username, form_data.password, db)

    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer"
    }
