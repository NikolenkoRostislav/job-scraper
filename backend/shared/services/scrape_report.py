from datetime import datetime, timezone

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models import ScrapeReport
from shared.schemas import DateRange
from shared.utils import NotFoundError


class ScrapeReportService:
    @staticmethod
    async def create_scrape_report(
        db: AsyncSession,
        target_website: str,
        scrape_start_time: datetime,
        scrape_stats,
        end_reason: str,
    ):
        scrape_report = ScrapeReport(
            target_website=target_website,
            scrape_started_at=scrape_start_time,
            scrape_finished_at=datetime.now(timezone.utc),
            total_jobs_scraped=scrape_stats.get("item_scraped_count", 0),
            warnings_count=scrape_stats.get("log_count/WARNING", 0),
            errors_count=scrape_stats.get("log_count/ERROR", 0),
            end_reason=end_reason,
        )

        db.add(scrape_report)
        await db.commit()
        return scrape_report

    @staticmethod
    async def get_scrape_reports(
        db: AsyncSession, source_spider: str, date_range: DateRange, failed_only: bool
    ):
        scrape_conditions = [ScrapeReport.target_website == source_spider]

        if date_range.start_time:
            scrape_conditions.append(
                ScrapeReport.scrape_started_at >= date_range.start_time
            )

        if date_range.end_time:
            scrape_conditions.append(
                ScrapeReport.scrape_started_at <= date_range.end_time
            )

        if failed_only:
            scrape_conditions.append(ScrapeReport.end_reason != "finished")

        scrape_reports_stmt = select(ScrapeReport).where(and_(*scrape_conditions))
        scrape_reports_result = await db.scalars(scrape_reports_stmt)
        scrape_reports = scrape_reports_result.all()
        return scrape_reports

    @staticmethod
    async def get_scrape_report(db: AsyncSession, report_id: int):
        stmt = select(ScrapeReport).where(ScrapeReport.id == report_id)
        result = await db.scalars(stmt)
        report = result.one_or_none()
        if not report:
            raise NotFoundError(f"Scrape report with id {report_id} not found")
        return report
