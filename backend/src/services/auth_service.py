from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User, RefreshToken
from src.utils.security import verify_password, create_access_token, decode_token, create_refresh_token, hash_token
from src.utils.exceptions import *


class AuthService:
    @staticmethod
    async def login(username: str, password: str, db: AsyncSession) -> dict:
        result = await db.scalars(select(User).where(User.username == username))
        user = result.one_or_none()

        if not user or not verify_password(password, user.password_hash):
            raise PermissionDeniedError("Invalid username or password")
        
        refresh_token_str = create_refresh_token(user.id)
        tokens = {
            "access_token": create_access_token(user.id), 
            "refresh_token": refresh_token_str
        }

        refresh_token = RefreshToken(
            token_hash = hash_token(refresh_token_str),
            user_id = user.id
        )
        db.add(refresh_token)
        await db.commit()

        return tokens
    
    @staticmethod
    async def refresh_token(token: str, db: AsyncSession) -> dict:
        try:
            token_data = decode_token(token)
            token_type = token_data["type"]
            if token_type != "refresh":
                raise Exception()
        except Exception:
            raise PermissionDeniedError("Invalid token")
        
        result = await db.scalars(select(RefreshToken).where(RefreshToken.token_hash == hash_token(token)))
        refresh_token = result.one_or_none()
        if not refresh_token:
            raise PermissionDeniedError("Invalid token")
        
        return create_access_token(refresh_token.user_id)
