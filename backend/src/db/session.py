from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import SessionLocal


async def get_db():
    async with SessionLocal() as session:
        yield session

DatabaseDep = Annotated[AsyncSession, Depends(get_db)]
