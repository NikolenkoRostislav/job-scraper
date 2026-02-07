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

from .base import JobExtractionStrategy
from .getinit import GetInItStrategy
from .relocateme import RelocateMeStrategy
from .sap import SapStrategy
from .siemens import SiemensStrategy
from .wearedevelopers import WeAreDevsStrategy
from .zalando import ZalandoStrategy
from .dice import DiceStrategy

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
