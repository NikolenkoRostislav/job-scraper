from src.scraping.strategies.base import JobExtractionStrategy


class GetInItStrategy(JobExtractionStrategy):
    def __init__(self):
        self.source_website = "https://www.get-in-it.de"

    def extract_title(self, response) -> str:
        self.title = response.css("h1::text").get(default="")
        return self.title

    def extract_location(self, response) -> str:
        self.location = response.css("div.ms-1-5.d-block p::text").get(default="")
        return self.location
    
    def extract_country(self, response):
        return "germany"

    def extract_description(self, response) -> str:
        self.description = "placeholder"
        return self.description
