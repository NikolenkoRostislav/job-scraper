"""
scraping.strategies

This package contains all job extraction strategies for IT-JobScraper.

Each strategy implements the JobExtractionStrategy interface to scrape
jobs from different websites, including:
- GetInIt
- RelocateMe
- SAP
- Siemens
- WeAreDevelopers
- Zalando
- Dice
"""

from scraping.strategies.base import JobExtractionStrategy
from scraping.strategies.getinit import GetInItStrategy
from scraping.strategies.relocateme import RelocateMeStrategy
from scraping.strategies.sap import SapStrategy
from scraping.strategies.siemens import SiemensStrategy
from scraping.strategies.wearedevelopers import WeAreDevsStrategy
from scraping.strategies.zalando import ZalandoStrategy
from scraping.strategies.dice import DiceStrategy

__all__ = [
    "JobExtractionStrategy",
    "GetInItStrategy",
    "RelocateMeStrategy",
    "SapStrategy",
    "SiemensStrategy",
    "WeAreDevsStrategy",
    "ZalandoStrategy",
    "DiceStrategy",
]
