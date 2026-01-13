from src.scraping.strategies.base import JobExtractionStrategy
from src.utils.parsers import try_extract_seniorities, try_extract_skills


class SapStrategy(JobExtractionStrategy):
    def __init__(self, countries_dict):
        self.countries_dict = countries_dict 

    def extract_url(self, response) -> str:
        return response.url

    def extract_title(self, response) -> str:
        self.title = response.css('span[data-careersite-propertyid="title"]::text').get(default="")
        return self.title

    def extract_location(self, response) -> str:
        return response.css('span.jobGeoLocation::text').get(default="")
    
    def extract_country(self, response) -> str:
        return self.countries_dict.get(response.meta['country'], "")
    
    def extract_description(self, response) -> str:
        elements = response.css('span.jobdescription p, span.jobdescription li')
        description_parts = []
        for element in elements:
            text = element.css('::text').getall()
            text = ' '.join(text).strip()
            if text:
                description_parts.append(text)
        self.description = '\n'.join(description_parts)
        return self.description
    
    def extract_skills(self, response) -> list[str]:
        return try_extract_skills(self.description)

    def extract_seniorities(self, response) -> list[str]:
        return try_extract_seniorities(self.title)
