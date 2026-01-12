import subprocess
from src.scheduler.app import celery


@celery.task() 
def scrape_task(spider_name: str):
    subprocess.run(["scrapy", "crawl", spider_name], check=True) 
