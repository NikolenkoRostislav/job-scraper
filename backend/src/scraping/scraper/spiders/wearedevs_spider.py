from pathlib import Path

import scrapy


class WeAreDevelopersSpider(scrapy.Spider):
    name = "wearedevs"
    start_urls = ["https://www.wearedevelopers.com/en/jobs"]

    def parse(self, response):
        for job in response.css(".wad4-job-card"):
            title = job.css("h3.wad4-job-card__title::text").get().strip()
            job_link = job.css("a.wad4-job-card__link::attr(href)").get()
            if job_link:
                yield response.follow(job_link, callback=self.parse_job, meta={'title': title})

    def parse_job(self, response):
        title = response.meta['title']
        sections = response.css("h2.wad4-job-details-section__title")
        contents = response.css("div.wad4-job-details__html-content")

        job_data = {
            'title': title,
            'link': response.url,
            'description': None
        }

        for h2, div in zip(sections, contents):
            section_title = h2.css("::text").get().strip().lower()
            section_text = " ".join(div.css("*::text").getall()).strip()

            if "job description" in section_title:
                job_data['description'] = section_text

        yield job_data
