from src.scraping.items import JobscraperItem
import scrapy


PAGINATION_LIMIT = 3

class WeAreDevelopersSpider(scrapy.Spider):
    name = "wearedevs"
    allowed_domains = ["wad-api.wearedevelopers.com", "www.wearedevelopers.com"]

    def start_requests(self):
        page = 1
        yield scrapy.Request(
            f"https://wad-api.wearedevelopers.com/api/v2/jobs/search?page={page}",
            callback=self.parse,
            meta={"page": page}
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
                }
            )

        next_page = response.meta["page"] + 1
        yield scrapy.Request(
            f"https://wad-api.wearedevelopers.com/api/v2/jobs/search?page={next_page}",
            callback=self.parse,
            meta={"page": next_page}
        )


    def parse_job(self, response):
        def get_section_text(section_name):
            sections = response.css("h2.wad4-job-details-section__title")
            for h2 in sections:
                section_title = h2.css("::text").get(default="").strip().lower()
                if section_name.lower() in section_title:
                    div = h2.xpath("following-sibling::div[1]")
                    return " ".join(div.css("*::text").getall()).strip()
            return ""

        job_item = JobscraperItem()
        job_item['url'] = response.url
        job_item['title'] = response.meta['title']
        job_item['skills'] = response.meta['skills']
        job_item['location'] = response.meta['location']
        job_item['seniority_levels'] = response.meta['seniority_levels']
        job_item['description'] = get_section_text("job description")

        yield job_item
