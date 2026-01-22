from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db, User
from src.api.exception_handler import handle_exceptions
from src.utils.security import decode_token
from src.utils.exceptions import *


DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(db: DatabaseDep, token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
        token_type = payload["type"]
        if token_type != "access":
            raise Exception
    except Exception:
        raise UnauthorizedError("Invalid or expired token")
    
    result = await db.scalars(select(User).where(User.id == user_id))
    user = result.one_or_none()

    if user is None:
        raise NotFoundError("User not found")
    return user

CurrentUserDep = Annotated[User, Depends(handle_exceptions(get_current_user))]


async def check_admin(user: CurrentUserDep):
    if not user.is_admin :
        raise PermissionDeniedError("Only admins can perform this action")

AdminDep = Annotated[bool, Depends(handle_exceptions(check_admin))]
