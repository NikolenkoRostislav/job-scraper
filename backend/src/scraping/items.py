from scrapy import Item, Field


class JobscraperItem(Item):
    url = Field()
    title = Field()
    description = Field()
    skills = Field()
    location = Field()
    country = Field()
    company = Field()
    source_website = Field()
    seniority_levels = Field()
    home_office = Field()
