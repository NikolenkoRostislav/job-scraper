from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import DateRange, WebsiteStats
from src.utils.classes.enums import LogLevel


class StatsService:
    @staticmethod
    async def get_logs(date_range: DateRange, log_name: str, log_level: LogLevel):
        pass

    @staticmethod
    async def get_job_count(date_range: DateRange, db: AsyncSession) -> int:
        pass


    @staticmethod
    async def get_outdated_jobs(cutoff_time: datetime, db: AsyncSession):
        pass


    @staticmethod
    async def get_stats(date_range: DateRange, source_website: str, db: AsyncSession) -> WebsiteStats:
        pass
