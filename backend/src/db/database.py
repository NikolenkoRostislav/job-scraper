from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import settings


DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
sync_engine = create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"), echo=False)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

SyncSessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False)

Base = declarative_base()
