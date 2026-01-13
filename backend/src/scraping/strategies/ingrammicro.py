from src.scraping.strategies.base import JobExtractionStrategy


class IngrammicroStrategy(JobExtractionStrategy):
    def extract_url(self, response) -> str:
        pass

    def extract_title(self, response) -> str:
        pass

    def extract_location(self, response) -> str:
        pass
    
    def extract_country(self, response) -> str:
        pass
    
    def extract_description(self, response) -> str:
        pass
    
    def extract_skills(self, response) -> list[str]:
        pass

    def extract_seniorities(self, response) -> list[str]:
        pass
