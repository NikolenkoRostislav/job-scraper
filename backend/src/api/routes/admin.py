from datetime import datetime

from fastapi import APIRouter, Query, Depends

from src.api.dependencies import DatabaseDep, AdminDep
from src.api.exception_handler import handle_exceptions
from src.services import JobService, ScrapeReportService, StatsService
from src.schemas import DateRange, WebsiteStats, JobListResponse, LogEntry, ScrapeReport
from src.utils import LogLevel


router = APIRouter(prefix="/admin", tags=["admin"])


@router.delete("/jobs/{job_id}")
@handle_exceptions
async def delete_job(db: DatabaseDep, admin: AdminDep, job_id: int):
    return await JobService.delete_job(job_id, db)


@router.get("/stats/logs", response_model=list[LogEntry])
@handle_exceptions
async def get_logs(admin: AdminDep, 
    log_name: str,
    log_level: LogLevel = LogLevel.WARNING,
    date_range: DateRange = Depends()
):
    return await StatsService.get_logs(date_range, log_name, log_level)


@router.get("/stats/jobs-count", response_model=int)
@handle_exceptions
async def get_job_count(db: DatabaseDep, admin: AdminDep, date_range: DateRange = Depends()):  
    return await JobService.get_job_count(date_range, db)


@router.get("/stats/outdated-jobs", response_model=JobListResponse)
@handle_exceptions
async def get_stale_jobs(db: DatabaseDep, admin: AdminDep,
    cutoff_time: datetime = Query(description="Jobs last seen before this datetime are considered outdated"),
):
    return await JobService.get_outdated_jobs(cutoff_time, db)


@router.get("/stats/{source_website}", response_model=WebsiteStats)
@handle_exceptions
async def get_website_stats(db: DatabaseDep, admin: AdminDep, source_website: str, date_range: DateRange = Depends()):
    return await StatsService.get_stats(date_range, source_website, db)


@router.get("/scrape-reports", response_model=list[ScrapeReport])
@handle_exceptions
async def get_scrape_reports(db: DatabaseDep, admin: AdminDep,
    source_spider: str,
    failed_only: bool = False, 
    date_range: DateRange = Depends()
):
    return await ScrapeReportService.get_scrape_reports(date_range, source_spider, failed_only, db)


@router.get("/scrape-reports/{report_id}", response_model=ScrapeReport)
@handle_exceptions
async def get_scrape_report(db: DatabaseDep, admin: AdminDep, report_id: int):
    return await ScrapeReportService.get_scrape_report(report_id, db)
