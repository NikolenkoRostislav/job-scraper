from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import ScrapeReport


class ScrapeReportService:
    @staticmethod
    async def create_scrape_report(
        target_website,
        scrape_start_time,
        scrape_stats,
        end_reason, 
        db: AsyncSession
    ):
        scrape_report = ScrapeReport(
            target_website=target_website,
            scrape_started_at=scrape_start_time,
            scrape_finished_at=datetime.now(),
            total_jobs_scraped=scrape_stats.get("item_scraped_count", 0),
            warnings_count=scrape_stats.get("log_count/WARNING", 0),
            errors_count=scrape_stats.get("log_count/ERROR", 0),
            end_reason=end_reason,
        )

        db.add(scrape_report)
        await db.commit()
        return scrape_report
