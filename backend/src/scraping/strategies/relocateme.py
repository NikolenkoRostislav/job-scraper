from src.scraping.strategies.base import JobExtractionStrategy


class RelocateMeStrategy(JobExtractionStrategy):
    def __init__(self):
        self.source_website = "https://relocate.me"

    def extract_title(self, response) -> str:
        self.title = response.css("h1::text").get(default="")
        return self.title

    def extract_location(self, response) -> str:
        self.location = response.css("div.job-info__country p::text").get(default="")
        return self.location

    def extract_description(self, response) -> str:
        description_info = response.css("div.job-info__description ::text").getall()
        self.description = " ".join(description_info)
        return self.description
    
    def extract_company(self, response):
        return response.css("div.job-info__company a::text").get(default="")
