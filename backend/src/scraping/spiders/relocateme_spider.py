import scrapy
from src.scraping.spiders.base import BaseSpider
from src.scraping.strategies.relocateme import RelocateMeStrategy


PAGINATION_LIMIT = 10


class RelocateMeSpider(BaseSpider):
    name = "relocateme"

    allowed_domains = ["relocate.me"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extraction_strategy = RelocateMeStrategy()

    async def start(self):
        url = f"https://relocate.me/international-jobs?page={1}"

        yield scrapy.Request(url, callback=self.parse, meta={"page": 1})

    def parse(self, response):
        jobs = response.css("div.job__title")
        job_hrefs = []
        for job in jobs:
            job_href = job.css("a::attr(href)").get()
            job_hrefs.append(job_href)

        if not job_hrefs or response.meta["page"] >= PAGINATION_LIMIT:
            return

        for job_href in job_hrefs:
            job_url = "https://relocate.me" + job_href 
            yield scrapy.Request(
                job_url,
                callback=self.parse_job,
            )

        next_page = response.meta["page"] + 1
        yield scrapy.Request(
            f"https://relocate.me/international-jobs?page={next_page}",
            callback=self.parse,
            meta={"page": next_page},
        )
