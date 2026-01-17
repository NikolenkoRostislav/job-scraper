import scrapy
from src.scraping.spiders.base import BaseSpider
from src.scraping.strategies import GetInItStrategy

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
        job_hrefs = [job["url"] for job in data["items"]["results"]]

        if not job_hrefs or response.meta["start_item"] >= PAGE_SIZE * PAGINATION_LIMIT:
            return
        
        yield from self.job_requests(
            response=response,
            job_links=job_hrefs,
        )

        next_start_item = response.meta["start_item"] + PAGE_SIZE
        yield scrapy.Request(
            f"https://www.get-in-it.de/api/v2/open/job/search?start={next_start_item}&limit={PAGE_SIZE}",
            callback=self.parse,
            headers={"X-Requested-With": "XMLHttpRequest"},
            meta={"start_item": next_start_item},
        )