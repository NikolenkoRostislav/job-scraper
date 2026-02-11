from datetime import timedelta

from celery import Celery

from core.config import settings


celery = Celery("tasks", broker=settings.celery.CELERY_BROKER_URL)

celery.autodiscover_tasks(["scheduler.tasks"])

celery.conf.update(
    worker_concurrency=2,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    broker_transport_options={"max_length": 1},
)

celery.conf.update(
    beat_schedule={
        "scrape_all_spiders": {
            "task": "scheduler.tasks.scrape_all_spiders",
            "schedule": timedelta(hours=settings.scrape.SCHEDULED_SCRAPE_DELAY_HOURS),
        },
        "delete_outdated_jobs": {
            "task": "scheduler.tasks.remove_outdated_jobs",
            "schedule": timedelta(hours=settings.scrape.SCHEDULED_CLEANUP_DELAY_HOURS),
        }
    }
)
