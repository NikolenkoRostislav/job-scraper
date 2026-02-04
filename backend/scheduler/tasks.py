from scheduler.app import celery
from scraping.scrape_all import scrape_all_spiders


@celery.task()
def scrape_all_spiders_task():
    scrape_all_spiders()
