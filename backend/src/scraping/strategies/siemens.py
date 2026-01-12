from src.scraping.strategies.base import JobExtractionStrategy
from src.utils.parsers import try_extract_seniorities, try_extract_skills, parse_country
from src.utils.normalizer import remove_extra_spaces


class SiemensStrategy(JobExtractionStrategy):
    def extract_url(self, response) -> str:
        return response.url

    def extract_title(self, response) -> str:
        self.title = response.css('h3.section__header__text__title title title--h3 title--white::text').get(default="").strip()
        return self.title

    def extract_location(self, response) -> str:
        self.location = response.css('ul.list--locations li.list__item::text').get(default="").strip()
        return self.location
    
    def extract_country(self, response) -> str:
        return parse_country(self.location)
    
    def extract_description(self, response) -> str:
        description = response.css('div.article__content__view__field__value ::text').getall()
        self.description_text = remove_extra_spaces(' '.join(description).strip())
        return self.description_text
    
    def extract_skills(self, response) -> list[str]:
        skills = set()
        skills.update(try_extract_skills(self.description_text))
        skills.update(try_extract_skills(self.title))
        return list(skills)

    def extract_seniorities(self, response) -> list[str]:
        return try_extract_seniorities(self.title)
