"""
src.scraping.strategies

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

from src.scraping.strategies.base import JobExtractionStrategy
from src.scraping.strategies.getinit import GetInItStrategy
from src.scraping.strategies.relocateme import RelocateMeStrategy
from src.scraping.strategies.sap import SapStrategy
from src.scraping.strategies.siemens import SiemensStrategy
from src.scraping.strategies.wearedevelopers import WeAreDevsStrategy
from src.scraping.strategies.zalando import ZalandoStrategy
from src.scraping.strategies.dice import DiceStrategy

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
