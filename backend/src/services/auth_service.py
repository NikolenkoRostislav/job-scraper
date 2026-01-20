from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User
from src.utils.security import verify_password, create_access_token
from src.utils.exceptions import *


class AuthService:
    @staticmethod
    async def login(username: str, password: str, db: AsyncSession) -> dict:
        result = await db.scalars(select(User).where(User.username == username))
        user = result.one_or_none()

        if not user or not verify_password(password, user.password_hash):
            raise PermissionDeniedError("Invalid username or password")
        
        tokens = {
            "access_token": create_access_token({"sub": str(user.id)}), # I'll add refresh token later
        }

        return {**tokens, "token_type": "bearer"}


