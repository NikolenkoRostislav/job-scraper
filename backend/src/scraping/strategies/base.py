from abc import ABC, abstractmethod


class JobExtractionStrategy(ABC):
    """Interface class for job extraction strategies"""
    @abstractmethod
    def extract_url(self, response) -> str:
        """Extract job url"""
        pass

    @abstractmethod
    def extract_title(self, response) -> str:
        """Extract job title"""
        pass

    @abstractmethod
    def extract_location(self, response) -> str:
        """Extract job location"""
        pass

    @abstractmethod
    def extract_country(self, response) -> str:
        """Extract job country"""
        pass

    @abstractmethod
    def extract_description(self, response) -> str:
        """Extract job description"""
        pass

    @abstractmethod
    def extract_skills(self, response) -> list[str]:
        """Extract job skills"""
        pass

    @abstractmethod
    def extract_seniorities(self, response) -> list[str]:
        """Extract job seniority levels"""
        pass
