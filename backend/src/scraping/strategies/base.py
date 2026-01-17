from urllib.parse import urlparse
from abc import ABC, abstractmethod
from src.utils.parsers import parse_country, try_extract_seniorities, try_extract_skills


class JobExtractionStrategy(ABC):
    """Interface class for job extraction strategies"""

    @abstractmethod
    def extract_location(self, response) -> str:
        """Extract job location"""
        pass

    @abstractmethod
    def extract_description(self, response) -> str:
        """Extract job description"""
        pass

    def extract_source_website(self, response) -> str:
        return urlparse(response.url).netloc

    def extract_url(self, response) -> str:
        return response.url

    def extract_title(self, response) -> str: 
        # A lot of sites have a single h1 with the job title so the default implementation can be used in such cases 
        self.title = response.css("h1::text").get(default="")
        return self.title

    def extract_company(self, response) -> str: 
        # Default implementation for company carreer portals, add the company name to init of the strategy
        return self.company

    def extract_country(self, response) -> str:
        # The country can often be parsed from the location, override if there is a better way for the specific site
        return parse_country(self.location)

    def extract_skills(self, response) -> list[str]:
        # Add additional logic if a site has a specific section for skills
        skills = set()
        skills.update(try_extract_skills(self.description))
        skills.update(try_extract_skills(self.title))
        return list(skills)

    def extract_seniorities(self, response) -> list[str]:
        # Add additional logic if a site has a specific section for seniorities
        seniorities = set()
        seniorities.update(try_extract_seniorities(self.description))
        seniorities.update(try_extract_seniorities(self.title))
        return list(seniorities)
