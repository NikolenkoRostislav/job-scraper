from abc import ABC
import scrapy
from src.scraping.items import JobscraperItem
from src.scraping.strategies.base import JobExtractionStrategy


class BaseSpider(scrapy.Spider, ABC):
    extraction_strategy: JobExtractionStrategy = None

    def parse_job(self, response):
        if not self.extraction_strategy:
            raise NotImplementedError(f"{self.__class__.__name__} must set extraction_strategy in __init__")

        job_item = JobscraperItem()
        job_item['url'] = self.extraction_strategy.extract_url(response)
        job_item['title'] = self.extraction_strategy.extract_title(response)
        job_item['location'] = self.extraction_strategy.extract_location(response)
        job_item['country'] = self.extraction_strategy.extract_country(response)
        job_item['description'] = self.extraction_strategy.extract_description(response)
        job_item['skills'] = self.extraction_strategy.extract_skills(response)
        job_item['seniority_levels'] = self.extraction_strategy.extract_seniorities(response)
        job_item['company'] = self.extraction_strategy.extract_company(response)

        yield job_item
