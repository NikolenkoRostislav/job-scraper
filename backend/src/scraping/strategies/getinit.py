from src.scraping.strategies.base import JobExtractionStrategy


class GetInItStrategy(JobExtractionStrategy):
    def __init__(self):
        self.company = "placeholder"
        
    def extract_location(self, response) -> str:
        self.location = response.css("div.ms-1-5.d-block p::text").get(default="")
        return self.location
    
    def extract_country(self, response):
        return "germany"

    def extract_description(self, response) -> str:
        self.description = "placeholder"
        return self.description
