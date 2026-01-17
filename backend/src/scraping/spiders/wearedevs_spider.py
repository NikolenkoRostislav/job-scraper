import scrapy
from src.scraping.spiders.base import BaseSpider
from src.scraping.strategies import WeAreDevsStrategy
from src.config import settings


PAGINATION_LIMIT = settings.GLOBAL_SCRAPE_PAGINATION_LIMIT


class WeAreDevelopersSpider(BaseSpider):
    name = "wearedevs"

    allowed_domains = ["wad-api.wearedevelopers.com", "www.wearedevelopers.com"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extraction_strategy = WeAreDevsStrategy()

    async def start(self):
        page = 1
        yield scrapy.Request(
            f"https://wad-api.wearedevelopers.com/api/v2/jobs/search?page={page}",
            callback=self.parse,
            meta={"page": page},
        )

    def parse(self, response):
        data = response.json()
        jobs = data.get("data", [])

        if not jobs or response.meta["page"] > PAGINATION_LIMIT:
            return

        for job in jobs:
            skills = job.get("skills", [])
            location = job.get("location", "").strip()
            title = job.get("title", "").strip()
            seniority_levels = job.get("seniorities", [])

            job_slug = job.get("slug")
            job_id = job.get("id")
            company_slug = job.get("company_slug", "")
            company_id = job.get("company_id", "")
            if not all([job_slug, company_slug, company_id, job_id]):
                continue

            job_link = f"https://www.wearedevelopers.com/en/companies/{company_id}/{company_slug}/{job_id}/{job_slug}"

            yield scrapy.Request(
                job_link,
                callback=self.parse_job,
                meta={
                    "skills": skills,
                    "title": title,
                    "location": location,
                    "seniority_levels": seniority_levels,
                },
            )

        next_page = response.meta["page"] + 1
        yield scrapy.Request(
            f"https://wad-api.wearedevelopers.com/api/v2/jobs/search?page={next_page}",
            callback=self.parse,
            meta={"page": next_page},
        )
