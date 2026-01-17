from src.scraping.strategies.base import JobExtractionStrategy


class ZalandoStrategy(JobExtractionStrategy):
    def __init__(self):
        self.company = "Zalando"

    def extract_location(self, response) -> str:
        self.location = response.xpath(
            '//dt[text()="Location"]/following-sibling::dd[1]/text()'
        ).get(default="")
        return self.location

    def extract_description(self, response) -> str:
        description_info = response.css(".prose ::text").getall()
        self.description = " ".join(description_info)
        return self.description
