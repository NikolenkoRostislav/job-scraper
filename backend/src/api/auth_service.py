from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User
from src.db.session import DatabaseDep
from src.utils.security import verify_password, create_access_token, decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthService:
    @staticmethod
    async def login(username: str, password: str, db: AsyncSession) -> dict:
        result = await db.scalars(select(User).where(User.username == username))
        user = result.one_or_none()

        if not user or not verify_password(password, user.password_hash):
            raise Exception("Invalid username or password")
        
        tokens = {
            "access_token": create_access_token({"sub": str(user.id)}), # I'll add refresh token later
        }

        return {**tokens, "token_type": "bearer"}

    @staticmethod
    async def get_current_user(db: DatabaseDep, token: str = Depends(oauth2_scheme)) -> User:
        try:
            payload = decode_token(token)
            user_id = int(payload.get("sub"))
        except Exception:
            raise Exception("Invalid or expired token")
        
        result = await db.scalars(select(User).where(User.id == user_id))
        user = result.one_or_none()

        if user is None:
            raise Exception("User not found")
        return user

CurrentUserDep = Annotated[User, Depends(AuthService.get_current_user)]
