from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from src.scheduler.app import celery

SPIDERS = [
    "wearedevelopers",
    "siemens",
    "sap",
    "getinit",
    "relocateme",
    "zalando",
    "dice",
]

def scrape_all_spiders():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    for spider_name in SPIDERS:
        process.crawl(spider_name)
    process.start()

@celery.task()
def scrape_all_spiders_task():
    scrape_all_spiders()
