import scrapy
from src.scraping.spiders.base import BaseSpider
from src.scraping.strategies.getinit import GetInItStrategy

PAGE_SIZE = 10
PAGINATION_LIMIT = 2


class GetInItSpider(BaseSpider):
    name = "getinit"

    allowed_domains = ["www.get-in-it.de"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extraction_strategy = GetInItStrategy()

    async def start(self):
        start_item = 0
        yield scrapy.Request(
            f"https://www.get-in-it.de/api/v2/open/job/search?start={start_item}&limit={PAGE_SIZE}",
            callback=self.parse,
            headers={"X-Requested-With": "XMLHttpRequest"},
            meta={"start_item": start_item},
        )

    def parse(self, response):
        data = response.json()

        if not data or response.meta["start_item"] >= PAGE_SIZE * PAGINATION_LIMIT:
            return
        yield 

        for job in data["items"]["results"]:
            job_url = "https://www.get-in-it.de" + job["url"]
            yield scrapy.Request(
                job_url,
                callback=self.parse_job
            )

        next_start_item = response.meta["start_item"] + PAGE_SIZE
        yield scrapy.Request(
            f"https://www.get-in-it.de/api/v2/open/job/search?start={next_start_item}&limit={PAGE_SIZE}",
            callback=self.parse,
            headers={"X-Requested-With": "XMLHttpRequest"},
            meta={"start_item": next_start_item},
        )