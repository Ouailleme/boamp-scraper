"""
BOAMP Scraper - Main scraper class
"""

import asyncio
import logging
from typing import List, Optional
from datetime import datetime
import re
from playwright.async_api import async_playwright, Browser, BrowserContext
from fake_useragent import UserAgent

from .models import Tender, TenderCategory, SearchFilters

logger = logging.getLogger("boamp-scraper")


class TenderScraper:
    """
    Main scraper class for BOAMP (French public tenders)
    
    Example:
        >>> scraper = TenderScraper()
        >>> tenders = scraper.search(keywords=["cloud"], limit=10)
        >>> print(f"Found {len(tenders)} tenders")
    """
    
    BASE_URL = "https://www.boamp.fr/pages/recherche/"
    
    def __init__(self, headless: bool = True):
        """
        Initialize scraper
        
        Args:
            headless: Run browser in headless mode (default: True)
        """
        self.headless = headless
        self.ua = UserAgent()
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._playwright = None
    
    async def _init_browser(self):
        """Initialize Playwright browser (stealth mode)"""
        if self._browser:
            return
        
        self._playwright = await async_playwright().start()
        
        # Stealth args (anti-detection)
        args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
        ]
        
        self._browser = await self._playwright.chromium.launch(
            headless=self.headless,
            args=args
        )
        
        self._context = await self._browser.new_context(
            user_agent=self.ua.random,
            viewport={'width': 1920, 'height': 1080},
            locale='fr-FR',
            timezone_id='Europe/Paris'
        )
        
        logger.info("✅ Browser initialized")
    
    async def _close_browser(self):
        """Close browser"""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        
        self._browser = None
        self._context = None
        self._playwright = None
    
    def _build_url(self, filters: SearchFilters) -> str:
        """Build BOAMP search URL with filters"""
        params = {
            "disposition": "chronologique",
            "nature": "marché",
            "famille": "F17"  # F17 = IT & Telecom
        }
        
        # Add keywords to URL if provided
        if filters.keywords:
            params["texte"] = " ".join(filters.keywords)
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.BASE_URL}?{query_string}"
    
    async def _scrape_page(self, filters: SearchFilters) -> List[Tender]:
        """Scrape one page of BOAMP"""
        await self._init_browser()
        
        page = await self._context.new_page()
        
        try:
            url = self._build_url(filters)
            logger.info(f"📍 Scraping: {url}")
            
            # Navigate
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await asyncio.sleep(2)  # Wait for JS rendering
            
            # Human-like behavior (scroll)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            await asyncio.sleep(1)
            
            # Extract tenders
            tenders = await self._extract_tenders(page, filters)
            
            logger.info(f"✅ Found {len(tenders)} tenders")
            return tenders
        
        except Exception as e:
            logger.error(f"❌ Scraping error: {e}")
            return []
        
        finally:
            await page.close()
    
    async def _extract_tenders(self, page, filters: SearchFilters) -> List[Tender]:
        """Extract tender data from page"""
        tenders = []
        
        # TODO: Fix real selectors for BOAMP (Week 1)
        # For now, use mock data to test the flow
        logger.warning("⚠️  Using MOCK DATA (real scraping TODO)")
        
        mock_tenders = [
            {
                "title": "Développement d'une plateforme Cloud Azure",
                "organisme": "Ministère de l'Intérieur",
                "budget": 250000,
                "category": TenderCategory.CLOUD_INFRASTRUCTURE
            },
            {
                "title": "Audit de cybersécurité et tests d'intrusion",
                "organisme": "Région Île-de-France",
                "budget": 180000,
                "category": TenderCategory.CYBERSECURITY
            },
            {
                "title": "Maintenance applicative Java / Spring Boot",
                "organisme": "CHU de Paris",
                "budget": 120000,
                "category": TenderCategory.MAINTENANCE
            },
            {
                "title": "Développement d'une application mobile iOS/Android",
                "organisme": "Ville de Lyon",
                "budget": 90000,
                "category": TenderCategory.MOBILE
            },
            {
                "title": "Migration infrastructure vers AWS",
                "organisme": "Ministère de l'Éducation Nationale",
                "budget": 300000,
                "category": TenderCategory.CLOUD_INFRASTRUCTURE
            },
            {
                "title": "Conseil en transformation digitale",
                "organisme": "Région Normandie",
                "budget": 150000,
                "category": TenderCategory.CONSULTING
            },
            {
                "title": "Développement site web institutionnel",
                "organisme": "Ville de Marseille",
                "budget": 75000,
                "category": TenderCategory.WEB
            },
            {
                "title": "Formation cybersécurité pour 50 agents",
                "organisme": "Ministère de la Justice",
                "budget": 100000,
                "category": TenderCategory.CYBERSECURITY
            },
            {
                "title": "Solution BI / Data Analytics",
                "organisme": "Région Bretagne",
                "budget": 200000,
                "category": TenderCategory.BI_DATA
            },
            {
                "title": "Support technique N2/N3 infrastructure",
                "organisme": "CHU de Toulouse",
                "budget": 110000,
                "category": TenderCategory.MAINTENANCE
            },
        ]
        
        # Filter mock data by keywords
        for mock in mock_tenders[:filters.limit]:
            # Simple keyword matching
            title_lower = mock["title"].lower()
            if filters.keywords:
                if not any(kw.lower() in title_lower for kw in filters.keywords):
                    continue
            
            tender = Tender(
                title=mock["title"],
                organisme=mock["organisme"],
                budget=mock["budget"],
                date_publication=datetime.now(),
                url=f"https://www.boamp.fr/avis/detail/mock-{mock['title'][:20].replace(' ', '-')}",
                category=mock["category"],
                region=None,
                description=None
            )
            
            if self._matches_filters(tender, filters):
                tenders.append(tender)
                
                if len(tenders) >= filters.limit:
                    break
        
        return tenders
    
    async def _parse_tender_element(self, element) -> Optional[Tender]:
        """Parse single tender element"""
        try:
            # Extract title
            title_elem = await element.query_selector("h2, h3, .title, .titre")
            title = await title_elem.inner_text() if title_elem else "N/A"
            
            # Extract organisme
            org_elem = await element.query_selector(".organisme, .organization")
            organisme = await org_elem.inner_text() if org_elem else "N/A"
            
            # Extract URL
            link_elem = await element.query_selector("a")
            url = await link_elem.get_attribute("href") if link_elem else ""
            if url and not url.startswith("http"):
                url = f"https://www.boamp.fr{url}"
            
            # Extract budget (if available)
            budget = 0
            budget_elem = await element.query_selector(".montant, .budget, .price")
            if budget_elem:
                budget_text = await budget_elem.inner_text()
                budget = self._parse_budget(budget_text)
            
            # Create tender object
            return Tender(
                title=title.strip(),
                organisme=organisme.strip(),
                budget=budget,
                date_publication=datetime.now(),
                url=url,
                category=TenderCategory.OTHER,
                region=None,
                description=None
            )
        
        except Exception as e:
            logger.debug(f"Error parsing element: {e}")
            return None
    
    def _parse_budget(self, text: str) -> int:
        """Parse budget from text"""
        try:
            # Extract numbers
            numbers = re.findall(r'\d+[\s,.]?\d*', text.replace(' ', ''))
            if numbers:
                # Convert to int
                num_str = numbers[0].replace(',', '').replace('.', '')
                return int(num_str)
        except:
            pass
        return 0
    
    def _matches_filters(self, tender: Tender, filters: SearchFilters) -> bool:
        """Check if tender matches filters"""
        # Budget filters
        if filters.budget_min and tender.budget < filters.budget_min:
            return False
        if filters.budget_max and tender.budget > filters.budget_max:
            return False
        
        # Region filter
        if filters.region and tender.region != filters.region:
            return False
        
        # Category filter
        if filters.category and tender.category != filters.category:
            return False
        
        return True
    
    async def search_async(
        self,
        keywords: Optional[List[str]] = None,
        category: Optional[TenderCategory] = None,
        budget_min: Optional[int] = None,
        budget_max: Optional[int] = None,
        region: Optional[str] = None,
        limit: int = 50
    ) -> List[Tender]:
        """
        Search for tenders (async)
        
        Args:
            keywords: List of keywords to search for
            category: Filter by tender category
            budget_min: Minimum budget in EUR
            budget_max: Maximum budget in EUR
            region: Filter by region
            limit: Maximum number of results (default: 50)
        
        Returns:
            List of Tender objects
        
        Example:
            >>> tenders = await scraper.search_async(
            ...     keywords=["cloud", "aws"],
            ...     budget_min=50000,
            ...     limit=10
            ... )
        """
        filters = SearchFilters(
            keywords=keywords or [],
            category=category,
            budget_min=budget_min,
            budget_max=budget_max,
            region=region,
            limit=limit
        )
        
        try:
            tenders = await self._scrape_page(filters)
            return tenders
        
        finally:
            await self._close_browser()
    
    def search(
        self,
        keywords: Optional[List[str]] = None,
        category: Optional[TenderCategory] = None,
        budget_min: Optional[int] = None,
        budget_max: Optional[int] = None,
        region: Optional[str] = None,
        limit: int = 50
    ) -> List[Tender]:
        """
        Search for tenders (sync wrapper)
        
        Args:
            keywords: List of keywords to search for
            category: Filter by tender category
            budget_min: Minimum budget in EUR
            budget_max: Maximum budget in EUR
            region: Filter by region
            limit: Maximum number of results (default: 50)
        
        Returns:
            List of Tender objects
        
        Example:
            >>> scraper = TenderScraper()
            >>> tenders = scraper.search(keywords=["cloud"], limit=10)
            >>> print(f"Found {len(tenders)} tenders")
        """
        return asyncio.run(self.search_async(
            keywords=keywords,
            category=category,
            budget_min=budget_min,
            budget_max=budget_max,
            region=region,
            limit=limit
        ))

