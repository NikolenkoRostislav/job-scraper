import subprocess
from src.scheduler.app import celery


@celery.task(time_limit=1800) 
def scrape_task():
    subprocess.run(["scrapy", "crawl", "wearedevs"], check=True)
