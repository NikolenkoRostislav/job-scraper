from src.scraping.strategies.base import JobExtractionStrategy
from src.utils.normalizer import normalize_string


class DiceStrategy(JobExtractionStrategy):
    def extract_company(self, response):
        return response.css("a.outline-offset-2::text").get(default="")
    
    def extract_location(self, response) -> str:
        self.location = response.css("span.text-sm.font-normal.text-font-light span::text").get(default="")
        return self.location

    def extract_description(self, response) -> str:
        description_info = response.css("div[class^='job-detail-description-module'] ::text").getall()
        self.description = " ".join(description_info)
        return self.description
    
    def extract_home_office(self, response):
        return "remote" in normalize_string(self.location)
    
    def extract_skills(self, response):
        skills = response.css("li div.font-medium::text").getall()
        skills = [normalize_string(skill) for skill in skills]
        return skills
