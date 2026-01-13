import scrapy
from src.scraping.spiders.base import BaseSpider
from src.scraping.strategies.ingrammicro import IngrammicroStrategy


PAGINATION_LIMIT = 4 #work in progress this is not finished!!!!!!!!!!

class IngrammicroSpider(BaseSpider): 
    name = "ingrammicro"

    allowed_domains = ["jobs.zalando.com"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extraction_strategy = IngrammicroStrategy()

    async def start(self):
        url = f"https://careers.ingrammicro.com/en/jobs/?search=&team=IT+and+Engineering&pagesize=20#results"
        
        yield scrapy.Request(
            url,
            callback=self.parse,
            meta={"page": 1}
        )

    def parse(self, response):
        job_hrefs = response.css('a[href^="/en/jobs/"]::attr(href)').getall()

        if not job_hrefs or response.meta["page"] >= PAGINATION_LIMIT:
            return

        for job_href in job_hrefs:
            if job_href:
                job_url = "https://jobs.zalando.com" + job_href
                yield scrapy.Request(
                    job_url,
                    callback=self.parse_job,
                )

        next_page = response.meta["page"] + 1
        yield scrapy.Request(
            f"https://jobs.zalando.com/en/jobs?category=Software+Engineering&category=IT+Consulting+%26+Operations&page={next_page}",
            callback=self.parse,
            meta={"page": next_page}
        )
