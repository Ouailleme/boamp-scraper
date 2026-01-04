"""
BOAMP Scraper - Scrape French public tenders in 3 lines of Python
"""

from .scraper import TenderScraper
from .models import Tender, TenderCategory

__version__ = "0.1.0"
__all__ = ["TenderScraper", "Tender", "TenderCategory"]

