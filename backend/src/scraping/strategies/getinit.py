from src.scraping.strategies.base import JobExtractionStrategy


class GetInItStrategy(JobExtractionStrategy):
    def extract_country(self, response):
        return "germany"
    
    def extract_company(self, response):
        return response.css("p[class^='JobHeaderRegular_companyTitle']::text").get(default="")
    
    def extract_location(self, response) -> str:
        self.location = response.css("div.ms-1-5.d-block p::text").get(default="")
        return self.location

    def extract_description(self, response) -> str:
        description_info = response.css("div.row div.col-12.offset-lg-1.col-lg-7 ::text").getall()
        self.description = " ".join(description_info)
        return self.description
