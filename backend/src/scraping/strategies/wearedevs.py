from src.scraping.strategies.base import JobExtractionStrategy
from src.utils.normalizer import normalize_string


# most of the logic is done in the parse method already, I'll refactor it later
class WeAreDevsStrategy(JobExtractionStrategy):  
    def extract_title(self, response) -> str:
        return response.meta["title"]

    def extract_location(self, response) -> str:
        self.location = response.meta["location"]
        return self.location

    def extract_description(self, response) -> str:
        sections = response.css("h2.wad4-job-details-section__title")
        for h2 in sections:
            section_title = normalize_string(h2.css("::text").get(default=""))
            if "job description" in section_title:
                div = h2.xpath("following-sibling::div[1]")
                return " ".join(div.css("*::text").getall()).strip()
        return ""

    def extract_skills(self, response) -> list[str]:
        return response.meta["skills"]

    def extract_seniorities(self, response) -> list[str]:
        return response.meta["seniority_levels"]

    def extract_company(self, response) -> str:
        return response.css("div.wad4-job-details__subtitles-entry ::text").get(
            default=""
        )  # the company name is always the first element in this div so if they change the order I'll fix it later
    
    def extract_home_office(self, response):
        if response.css("div.wad4-common-chip.wad4-common-chip--remote"):
            return True
        return False
