from src.scraping.items import JobscraperItem
import scrapy


class WeAreDevelopersSpider(scrapy.Spider):
    name = "wearedevs"
    start_urls = ["https://www.wearedevelopers.com/en/jobs"]

    def parse(self, response):
        for job in response.css(".wad4-job-card"):
            title = job.css("h3.wad4-job-card__title::text").get(default="").strip()
            seniority_levels = job.css("div.wad4-common-chip--seniority span.wad4-common-chip__label::text").getall()
            location = job.css("span.wad4-job-card__info--light::text").get(default="").strip()
            job_link = job.css("a.wad4-job-card__link::attr(href)").get()
            if job_link:
                yield response.follow(job_link, callback=self.parse_job, meta={'title': title, 'location': location, 'seniority_levels': seniority_levels})

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
        job_item['location'] = response.meta['location']
        job_item['seniority_levels'] = response.meta['seniority_levels']
        job_item['description'] = get_section_text("job description")

        skills = response.css("div.wad4-job-details__skills span.wad4-common-chip__label::text").getall()
        job_item['skills'] = [ skill.strip() for skill in skills if skill.strip() ]

        yield job_item
