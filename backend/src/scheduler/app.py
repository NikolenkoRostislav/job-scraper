from datetime import timedelta
from celery import Celery
from src.config import settings


celery = Celery("tasks", broker=settings.CELERY_BROKER_URL)

celery.autodiscover_tasks(["src.scheduler.tasks"])

celery.conf.update(
    beat_schedule={
        "scrape_wearedevs": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=3),
            "args": ("wearedevs"),
        },
        "scrape_siemens": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=3),
            "args": ("siemens"),
        },
        "scrape_sap": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=3),
            "args": ("sap"),
        },
        "scrape_getinit": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=3),
            "args": ("getinit"),
        },
        "scrape_relocateme": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=3),
            "args": ("relocateme"),
        },
        "scrape_zalando": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=3),
            "args": ("zalando"),
        },
    }
)
