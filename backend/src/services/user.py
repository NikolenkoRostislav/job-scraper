from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import User
from src.schemas import UserCreateBase
from src.utils import get_password_hash, AlreadyExistsError


async def _get_user_by_field(field_name: str, value, db: AsyncSession) -> User | None:
    field = getattr(User, field_name)
    result = await db.scalars(select(User).where(field == value))
    user = result.one_or_none()
    return user


class UserService():
    @staticmethod
    async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
        return await _get_user_by_field('email', email, db)
    

    @staticmethod
    async def get_user_by_username(username: str, db: AsyncSession) -> User | None:
        return await _get_user_by_field('username', username, db)


    @staticmethod
    async def get_user_by_id(id: str, db: AsyncSession) -> User | None:
        return await _get_user_by_field('id', id, db)
    

    @staticmethod
    async def create_user(user_data: UserCreateBase, db: AsyncSession) -> User:
        existing_email = await UserService.get_user_by_email(user_data.email, db)
        if existing_email:
            raise AlreadyExistsError("Email already in use")
        
        existing_username = await UserService.get_user_by_username(user_data.username, db)
        if existing_username:
            raise AlreadyExistsError("Username already in use")

        if hasattr(user_data, "password"):
            hashed_password = get_password_hash(user_data.password)
            user = User(
                email=user_data.email,
                username=user_data.username,
                password_hash=hashed_password
            )
        else:
            user = User(
                email=user_data.email,
                username=user_data.username,
                google_id=user_data.google_id
            )
        db.add(user)
        await db.commit()
        return user
