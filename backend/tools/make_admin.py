import asyncio

from sqlalchemy import select

from src.core.database import SessionLocal
from src.models import User


async def make_admin(user_id: int):
    async with SessionLocal() as db:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            print(f"User with id={user_id} not found")
            return

        if user.is_admin:
            print(f"User {user.username} is already an admin")
            return

        user.is_admin = True
        await db.commit()
        print(f"User {user.username} is now an admin!")


if __name__ == "__main__":
    user_id = int(input("Enter user id"))
    asyncio.run(make_admin(user_id))
