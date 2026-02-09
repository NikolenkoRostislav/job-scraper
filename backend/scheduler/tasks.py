import asyncio
from datetime import timedelta, datetime, timezone

from core.database import SessionLocal
from scheduler.app import celery
from scraping.scrape_all import scrape_all_spiders
from shared.services import JobService


@celery.task()
def scrape_all_spiders_task():
    scrape_all_spiders()


DAYS_UNTIL_OUTDATED = 7

async def _remove_outdated_jobs():
    async with SessionLocal() as db:
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=DAYS_UNTIL_OUTDATED)
        await JobService.remove_outdated_jobs(db, cutoff_time)

@celery.task()
def remove_outdated_jobs():
    asyncio.run(_remove_outdated_jobs())