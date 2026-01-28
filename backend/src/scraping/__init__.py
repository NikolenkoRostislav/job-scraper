"""
src.scraping

This package contains all web scraping logic for IT-JobScraper, using Scrapy and custom strategies.

- items.py:
    Defines the Scrapy Item classes, which represent structured data extracted from job listings.

- middlewares.py:
    Custom Scrapy middlewares.

- pipelines.py:
    Scrapy pipelines to process scraped items (normalizing and storing them in the database).

- settings.py:
    Scrapy project settings.

- spiders:
    Contains all Scrapy spider definitions, each responsible for crawling a specific job portal:
    - base.py: Base spider class with shared scraping logic.
    - wearedevelopers.py, siemens.py, sap.py, getinit.py, relocateme.py, zalando.py, dice.py: Site-specific spiders.

- strategies:
    Contains extraction strategies for each portal, defining how to parse listings and extract data:
    - base.py: Base extraction strategy with common parsing utilities.
    - wearedevelopers.py, siemens.py, sap.py, getinit.py, relocateme.py, zalando.py, dice.py: Portal-specific strategies.

"""
