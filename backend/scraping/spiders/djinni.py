import scrapy

from scraping.spiders.base import BaseSpider
from scraping.strategies.djinni import DjinniStrategy


class DjinniSpider(BaseSpider):
    name = "djinni"

    allowed_domains = ["djinni.co"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extraction_strategy = DjinniStrategy()

    async def start(self):
        page = 1
        url = f"https://djinni.co/jobs/?page={page}"

        yield scrapy.Request(url, callback=self.parse, meta={"page": page})

    def parse(self, response):
        jobs = response.css("li[id^='job-item-']")
        
        for job in jobs:
            company = job.css("a[data-analytics='company_page']::text").get(default="").strip()

            work_texts = job.css("div.fw-medium span.text-nowrap::text").getall()
            combined = " ".join(work_texts).lower()
            home_office = ("тільки віддалено" in combined) or ("гібридний формат роботи" in combined)

            location = job.css("span.location-text::text").get(default="").strip()

            relative_url = job.css("a.job-item__title-link::attr(href)").get()

            if not relative_url:
                continue

            job_link = response.urljoin(relative_url)

            yield scrapy.Request(
                job_link,
                callback=self.parse_job,
                meta={
                    "company": company,
                    "location": location,
                    "home_office": home_office,
                },
            )

        next_page = response.meta["page"] + 1
        yield scrapy.Request(
            f"https://djinni.co/jobs/?page={next_page}",
            callback=self.parse,
            meta={"page": next_page},
        )
