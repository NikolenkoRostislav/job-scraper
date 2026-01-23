from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from src.schemas import DateRange, WebsiteStats
from src.utils.classes.enums import LogLevel
from src.db.models import JobListing


class StatsService:
    @staticmethod
    async def get_logs(date_range: DateRange, log_name: str, log_level: LogLevel):
        pass

    @staticmethod
    async def get_job_count(date_range: DateRange, db: AsyncSession) -> int:
        stmt = select(func.count(JobListing.id))
        
        conditions = []
        
        if date_range.start_time:
            conditions.append(JobListing.created_at >= date_range.start_time)
        
        if date_range.end_time:
            conditions.append(JobListing.created_at <= date_range.end_time)
        
        if conditions:
            stmt = stmt.where(and_(*conditions))
        
        result = await db.scalar(stmt)
        return result or 0


    @staticmethod
    async def get_outdated_jobs(cutoff_time: datetime, db: AsyncSession):
        pass


    @staticmethod
    async def get_stats(date_range: DateRange, source_website: str, db: AsyncSession) -> WebsiteStats:
        pass
