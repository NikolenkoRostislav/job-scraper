from scraping.strategies.base import JobExtractionStrategy


class DjinniStrategy(JobExtractionStrategy):
    def extract_title(self, response):
        self.title = response.css("h1 span::text").get(default="").strip()
        return self.title

    def extract_description(self, response) -> str:
        description_info = response.css("div.job-post__description ::text").getall()
        self.description = " ".join(description_info).strip()
        return self.description
    
    def extract_company(self, response) -> str: 
        return response.meta["company"]
    
    def extract_location(self, response) -> str:
        self.location = response.meta["location"]
        return self.location
    
    def extract_home_office(self, response) -> bool:
        return response.meta["home_office"]
