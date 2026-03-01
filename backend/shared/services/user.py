from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models import User
from shared.schemas import UserCreateBase
from shared.utils import AlreadyExistsError
from core.security import get_password_hash


async def _get_user_by_field(db: AsyncSession, field_name: str, value) -> User | None:
    field = getattr(User, field_name)
    result = await db.scalars(select(User).where(field == value))
    user = result.one_or_none()
    return user


class UserService:
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        return await _get_user_by_field(db, "email", email)

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
        return await _get_user_by_field(db, "username", username)

    @staticmethod
    async def get_user_by_id(db: AsyncSession, id: str) -> User | None:
        return await _get_user_by_field(db, "id", id)

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreateBase) -> User:
        existing_email = await UserService.get_user_by_email(db, user_data.email)
        if existing_email:
            raise AlreadyExistsError("Email already in use")

        existing_username = await UserService.get_user_by_username(
            db, user_data.username
        )
        if existing_username:
            raise AlreadyExistsError("Username already in use")

        if hasattr(user_data, "password"):
            hashed_password = get_password_hash(user_data.password)
            user = User(
                email=user_data.email,
                username=user_data.username,
                password_hash=hashed_password,
            )
        else:
            user = User(
                email=user_data.email,
                username=user_data.username,
                google_id=user_data.google_id,
            )
        db.add(user)
        await db.commit()
        return user
