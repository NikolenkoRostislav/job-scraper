from src.scraping.strategies.base import JobExtractionStrategy
from src.utils.parsers import parse_country, try_extract_seniorities, try_extract_skills


class ZalandoStrategy(JobExtractionStrategy):
    def extract_url(self, response) -> str:
        return response.url

    def extract_title(self, response) -> str:
        self.title = response.css("h1.mb-6.font-bold::text").get(default="")
        return self.title

    def extract_location(self, response) -> str:
        self.location = response.xpath('//dt[text()="Location"]/following-sibling::dd[1]/text()').get(default="")
        return self.location
    
    def extract_country(self, response) -> str:
        return parse_country(self.location)
    
    def extract_description(self, response) -> str:
        description = response.css(".prose ::text").getall()
        self.description_text = ' '.join(description)
        return self.description_text
    
    def extract_skills(self, response) -> list[str]:
        skills = set()
        skills.update(try_extract_skills(self.description_text))
        skills.update(try_extract_skills(self.title))
        return list(skills)

    def extract_seniorities(self, response) -> list[str]:
        seniorities = set()
        seniorities.update(try_extract_seniorities(self.description_text))
        seniorities.update(try_extract_seniorities(self.title))
        return list(seniorities)
