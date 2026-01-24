from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from src.schemas import DateRange, WebsiteStats, ScrapeReport as ScrapeReportSchema
from src.utils.classes.enums import LogLevel
from src.db.models import JobListing, ScrapeReport


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
        stmt = select(JobListing).where(JobListing.last_seen_at < cutoff_time)
        
        result = await db.scalars(stmt)
        jobs = result.all()
        
        return {"jobs": jobs, "size": len(jobs)}


    @staticmethod
    async def get_stats(date_range: DateRange, source_website: str, db: AsyncSession) -> WebsiteStats:
        job_stmt = select(func.count(JobListing.id))
        job_conditions = [JobListing.source_website == source_website]
        
        if date_range.start_time:
            job_conditions.append(JobListing.created_at >= date_range.start_time)
        
        if date_range.end_time:
            job_conditions.append(JobListing.created_at <= date_range.end_time)
        
        if job_conditions:
            job_stmt = job_stmt.where(and_(*job_conditions))
        
        job_count = await db.scalar(job_stmt) or 0
        
        scrape_stmt = select(func.count(ScrapeReport.id))
        scrape_conditions = [ScrapeReport.target_website == source_website]
        
        if date_range.start_time:
            scrape_conditions.append(ScrapeReport.scrape_started_at >= date_range.start_time)
        
        if date_range.end_time:
            scrape_conditions.append(ScrapeReport.scrape_started_at <= date_range.end_time)
        
        if scrape_conditions:
            scrape_stmt = scrape_stmt.where(and_(*scrape_conditions))
        
        scrape_count = await db.scalar(scrape_stmt) or 0
        
        scrape_reports_stmt = select(ScrapeReport).where(and_(*scrape_conditions))
        scrape_reports_result = await db.scalars(scrape_reports_stmt)
        scrape_reports = scrape_reports_result.all()
        
        return WebsiteStats(
            job_count=job_count,
            scrape_count=scrape_count,
            scrape_reports=scrape_reports,
            date_range=date_range
        )
