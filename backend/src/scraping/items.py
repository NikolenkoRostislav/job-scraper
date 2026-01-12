from scrapy import Item, Field


class JobscraperItem(Item):
    title = Field()
    description = Field()
    skills = Field()
    location = Field()
    country = Field()
    seniority_levels = Field()
    url = Field()
