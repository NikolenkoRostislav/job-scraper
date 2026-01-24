from src.scheduler.tasks import scrape_task


# For triggering the scrape task manually
spider_names = [
    "relocateme",
    "wearedevs",
    "siemens",
    "getinit",
    "zalando",
    "dice",
    "sap",
]

for spider_name in spider_names:
    scrape_task.delay(spider_name)
