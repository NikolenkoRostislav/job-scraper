import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.chdir(Path(__file__).resolve().parent.parent)

from scraping.scrape_all import scrape_all_spiders


scrape_all_spiders()