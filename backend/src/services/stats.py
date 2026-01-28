import re
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from src.schemas import DateRange, WebsiteStats, LogEntry
from src.utils import LogLevel, LOG_LEVEL_PRIORITY, get_log_file
from src.db import JobListing
from src.services.scrape_report import ScrapeReportService


class StatsService:
    @staticmethod
    async def get_logs(date_range: DateRange, log_name: str, log_level: LogLevel) -> list[LogEntry]:
        """
        Retrieve and filter log entries from a log file.

        This function reads a log file, parses log lines using a fixed log format,
        and returns structured log entries filtered by:
        - a time range (start and/or end time)
        - a minimum log level threshold

        Args:
            date_range (DateRange):
                Time range to filter logs by. If provided, only log entries within
                the specified range are returned.
            log_name (str):
                Filename of the log to read.
            log_level (LogLevel):
                Minimum log level to include. Entries with a lower priority level
                are excluded.

        Returns:
            list[LogEntry]:
                A list of parsed and filtered log entries ordered as they appear
                in the log file.
        """
    
        if log_level:
            requested_level = LOG_LEVEL_PRIORITY.get(log_level.value)

        log_file = get_log_file(log_name, must_exist=True)
        with open(log_file, "r", encoding="utf-8") as f:
            log_str_list = f.readlines() 

        log_pattern = re.compile(
            r"^(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),(?P<msec>\d{3}) \[(?P<level>\w+)\] (?P<source>[^:]+): (?P<message>.+)$"
        )

        log_entries = []

        for log_str in log_str_list:
            log_str = log_str.strip()
            match = log_pattern.match(log_str)
            if not match:
                continue

            log_date_str = match.group("date") + "," + match.group("msec")
            log_level_str = match.group("level")
            log_source_str = match.group("source")
            log_message_str = match.group("message")

            timestamp = datetime.strptime(log_date_str.strip(), "%Y-%m-%d %H:%M:%S,%f").replace(tzinfo=timezone.utc)

            if date_range.start_time and timestamp > date_range.start_time:
                continue
            if date_range.end_time and timestamp < date_range.end_time:
                continue

            if log_level:
                entry_level = LOG_LEVEL_PRIORITY.get(log_level_str)
                if entry_level < requested_level:
                    continue

            log_entry = LogEntry(
                timestamp=timestamp,
                level=log_level_str,
                source=log_source_str,
                message=log_message_str
            )
            log_entries.append(log_entry)

        return log_entries


    @staticmethod
    async def get_stats(date_range: DateRange, source_website: str, db: AsyncSession) -> WebsiteStats:
        """
        Retrieve aggregated statistics for a specific website within a given date range.

        This method calculates:
        - The total number of job listings created for the given source website
        - The total number of scrape runs executed
        - The number of failed scrape runs (scrapes not ending with "finished")

        The job listing count is filtered by the provided date range if start_time
        and/or end_time are specified.

        Args:
            date_range (DateRange): Date range used to filter job listings and scrape reports.
            source_website (str): Identifier of the website being analyzed.
            db (AsyncSession): Active asynchronous database session.

        Returns:
            WebsiteStats: An object containing job count, scrape count,
            failed scrape count, and the applied date range.
        """

        job_stmt = select(func.count(JobListing.id))
        job_conditions = [JobListing.source_website == source_website]
        
        if date_range.start_time:
            job_conditions.append(JobListing.created_at >= date_range.start_time)
        
        if date_range.end_time:
            job_conditions.append(JobListing.created_at <= date_range.end_time)
        
        if job_conditions:
            job_stmt = job_stmt.where(and_(*job_conditions))
        
        job_count = await db.scalar(job_stmt) or 0
        
        scrape_reports = await ScrapeReportService.get_scrape_reports(date_range, source_website, failed_only=False, db=db)
        scrape_count = len(scrape_reports)
        failed_scrape_count = len([scrape_report for scrape_report in scrape_reports if (scrape_report.end_reason != "finished")])

        return WebsiteStats(
            job_count=job_count,
            scrape_count=scrape_count,
            failed_scrape_count=failed_scrape_count,
            date_range=date_range
        )
