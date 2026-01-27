from datetime import timedelta
from celery import Celery
from src.config import settings


celery = Celery("tasks", broker=settings.CELERY_BROKER_URL)

celery.autodiscover_tasks(["src.scheduler.tasks"])

celery.conf.update(
    worker_concurrency=1,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    broker_transport_options={"max_length": 1},
)

celery.conf.update(
    beat_schedule={
        "scrape_all_spiders": {
            "task": "src.scheduler.tasks.scrape_all_spiders",
            "schedule": timedelta(hours=settings.SCHEDULED_SCRAPE_DELAY_HOURS),
        },
    }
)
