from src.scraping.strategies.base import JobExtractionStrategy


class SiemensStrategy(JobExtractionStrategy):
    def extract_title(self, response) -> str:
        self.title = response.css('h3.section__header__text__title.title.title--h3.title--white::text').get(default="")
        return self.title

    def extract_location(self, response) -> str:
        self.location = response.css('ul.list--locations li.list__item::text').get(default="")
        return self.location
    
    def extract_description(self, response) -> str:
        description_info = response.css('div.article__content__view__field__value ::text').getall()
        self.description = ' '.join(description_info)
        return self.description
