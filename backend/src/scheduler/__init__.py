"""
src.scheduler

This package handles scheduled scraping tasks for IT-JobScraper using Celery and Scrapy.

- app.py:
    Configures the Celery app for background task execution.
    - Sets up the broker URL from settings.
    - Autodiscover tasks in `src.scheduler.tasks`.
    - Configures worker concurrency, prefetch behavior, and task acknowledgment.
    - Defines the Celery beat schedule for periodic tasks (e.g., `scrape_all_spiders`).

- tasks.py:
    Defines the actual scraping tasks to run.
    - `scrape_all_spiders`: Runs all spiders using Scrapy's CrawlerProcess.
    - `scrape_all_spiders_task`: Celery task wrapper around `scrape_all_spiders` for scheduled execution.

"""
