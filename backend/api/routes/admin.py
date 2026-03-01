from datetime import datetime

from fastapi import APIRouter, Depends, Query
from shared.schemas import (
    DateRange,
    JobListResponse,
    LogEntry,
    ScrapeReport,
    WebsiteStats,
)
from shared.services import JobService, ScrapeReportService, StatsService
from shared.utils import LogLevel, SourceWebsite

from api.dependencies import DatabaseDep, check_admin
from api.exception_handler import responses_for

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(check_admin)])


@router.delete(
    "/jobs/{job_id}", status_code=204, responses=responses_for(401, 403, 404)
)
async def delete_job(db: DatabaseDep, job_id: int):
    return await JobService.delete_job(db, job_id)


@router.get(
    "/stats/logs", response_model=list[LogEntry], responses=responses_for(401, 403)
)
async def get_logs(
    log_name: str,
    log_level: LogLevel = LogLevel.WARNING,
    date_range: DateRange = Depends(),
):
    return await StatsService.get_logs(
        log_name, log_level=log_level, date_range=date_range
    )


@router.get("/stats/jobs-count", response_model=int, responses=responses_for(401, 403))
async def get_job_count(db: DatabaseDep, date_range: DateRange = Depends()):
    return await JobService.get_job_count(db, date_range=date_range)


@router.get(
    "/stats/outdated-jobs",
    response_model=JobListResponse,
    responses=responses_for(401, 403),
)
async def get_stale_jobs(
    db: DatabaseDep,
    cutoff_time: datetime = Query(
        description="Jobs last seen before this datetime are considered outdated"
    ),
):
    return await JobService.get_outdated_jobs(db, cutoff_time=cutoff_time)


@router.get(
    "/stats/{source_website}",
    response_model=WebsiteStats,
    responses=responses_for(401, 403),
)
async def get_website_stats(
    db: DatabaseDep, source_website: SourceWebsite, date_range: DateRange = Depends()
):
    return await StatsService.get_stats(db, source_website.value, date_range=date_range)


@router.get(
    "/scrape-reports",
    response_model=list[ScrapeReport],
    responses=responses_for(401, 403),
)
async def get_scrape_reports(
    db: DatabaseDep,
    source_spider: SourceWebsite,
    failed_only: bool = False,
    date_range: DateRange = Depends(),
):
    return await ScrapeReportService.get_scrape_reports(
        db, source_spider.value, date_range=date_range, failed_only=failed_only
    )


@router.get(
    "/scrape-reports/{report_id}",
    response_model=ScrapeReport,
    responses=responses_for(401, 403, 404),
)
async def get_scrape_report(db: DatabaseDep, report_id: int):
    return await ScrapeReportService.get_scrape_report(db, report_id)
