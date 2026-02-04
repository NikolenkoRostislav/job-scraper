from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


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
