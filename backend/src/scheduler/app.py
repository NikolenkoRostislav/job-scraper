from datetime import timedelta
from celery import Celery
from src.config import settings


celery = Celery("tasks", broker=settings.CELERY_BROKER_URL)

celery.autodiscover_tasks(["src.scheduler.tasks"])

celery.conf.update(
    beat_schedule={
        "scrape_wearedevs": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=settings.SCHEDULED_SCRAPE_DELAY_HOURS),
            "args": ("wearedevelopers"),
        },
        "scrape_siemens": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=settings.SCHEDULED_SCRAPE_DELAY_HOURS),
            "args": ("siemens"),
        },
        "scrape_sap": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=settings.SCHEDULED_SCRAPE_DELAY_HOURS),
            "args": ("sap"),
        },
        "scrape_getinit": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=settings.SCHEDULED_SCRAPE_DELAY_HOURS),
            "args": ("getinit"),
        },
        "scrape_relocateme": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=settings.SCHEDULED_SCRAPE_DELAY_HOURS),
            "args": ("relocateme"),
        },
        "scrape_zalando": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=settings.SCHEDULED_SCRAPE_DELAY_HOURS),
            "args": ("zalando"),
        },
        "scrape_dice": {
            "task": "src.scheduler.tasks.scrape_task",
            "schedule": timedelta(hours=3),
            "args": ("dice"),
        },
    }
)
