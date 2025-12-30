from scrapy import Item, Field


class JobscraperItem(Item):
    title = Field()
    description = Field()
    url = Field()
