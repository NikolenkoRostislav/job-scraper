from abc import ABC, abstractmethod
from src.utils.parsers import parse_country, try_extract_seniorities, try_extract_skills


class JobExtractionStrategy(ABC):
    """Interface class for job extraction strategies"""
    @abstractmethod
    def extract_title(self, response) -> str:
        """Extract job title"""
        pass

    @abstractmethod
    def extract_location(self, response) -> str:
        """Extract job location"""
        pass

    @abstractmethod
    def extract_description(self, response) -> str:
        """Extract job description"""
        pass

    @abstractmethod
    def extract_company(self, response) -> str:
        """Extract company name"""
        pass

    def extract_url(self, response) -> str:
        return response.url

    def extract_country(self, response) -> str:
        return parse_country(self.location)

    def extract_skills(self, response) -> list[str]:
        skills = set()
        skills.update(try_extract_skills(self.description))
        skills.update(try_extract_skills(self.title))
        return list(skills)

    def extract_seniorities(self, response) -> list[str]:
        seniorities = set()
        seniorities.update(try_extract_seniorities(self.description))
        seniorities.update(try_extract_seniorities(self.title))
        return list(seniorities)
