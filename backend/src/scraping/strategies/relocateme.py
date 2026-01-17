from src.scraping.strategies.base import JobExtractionStrategy
from src.utils.normalizer import normalize_string

class RelocateMeStrategy(JobExtractionStrategy):
    def extract_location(self, response) -> str:
        self.location = response.css("div.job-info__country p::text").get(default="")
        return self.location

    def extract_description(self, response) -> str:
        description_info = response.css("div.job-info__description ::text").getall()
        self.description = " ".join(description_info)
        return self.description
    
    def extract_company(self, response):
        return response.css("div.job-info__company a::text").get(default="")
    
    def extract_home_office(self, response):
        return "remote" in normalize_string(self.location)
