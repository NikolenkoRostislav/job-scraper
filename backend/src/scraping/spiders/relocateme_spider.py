import scrapy
from src.scraping.spiders.base import BaseSpider
from src.scraping.strategies import RelocateMeStrategy
from src.config import settings


PAGINATION_LIMIT = settings.GLOBAL_SCRAPE_PAGINATION_LIMIT


class RelocateMeSpider(BaseSpider):
    name = "relocateme"

    allowed_domains = ["relocate.me"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extraction_strategy = RelocateMeStrategy()

    async def start(self):
        page = 1
        url = f"https://relocate.me/international-jobs?page={page}"

        yield scrapy.Request(url, callback=self.parse, meta={"page": page})

    def parse(self, response):
        job_hrefs = response.css("div.job__title a::attr(href)").getall()

        if not job_hrefs or response.meta["page"] >= PAGINATION_LIMIT:
            return

        yield from self.job_requests(
            response=response,
            job_links=job_hrefs,
        )

        next_page = response.meta["page"] + 1
        yield scrapy.Request(
            f"https://relocate.me/international-jobs?page={next_page}",
            callback=self.parse,
            meta={"page": next_page},
        )
