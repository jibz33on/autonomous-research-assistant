"""Web scraper for extracting article content."""

import requests
from bs4 import BeautifulSoup
from readability import Document
from typing import Optional, List, Dict
from src.utils.config import settings
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


class WebScraper:
    """Scrapes web pages and extracts main content."""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize scraper.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        logger.info("Web scraper initialized")
    
    def scrape_url(self, url: str) -> Optional[str]:
        """
        Scrape a single URL and extract main content.
        
        Args:
            url: URL to scrape
            
        Returns:
            Cleaned text content, or None if failed
        """
        try:
            logger.info(f"Scraping: {url}")
            
            # Download HTML
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            # Extract main content using readability
            doc = Document(response.text)
            html_content = doc.summary()
            
            # Convert to clean text
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            
            # Remove extra whitespace
            text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
            
            logger.info(f"Scraped {len(text)} characters from {url}")
            return text
            
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {str(e)}")
            return None
    
    def scrape_multiple(self, urls: List[str]) -> Dict[str, Optional[str]]:
        """
        Scrape multiple URLs.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            Dict mapping url -> content (None if failed)
        """
        results = {}
        
        for url in urls:
            content = self.scrape_url(url)
            results[url] = content
        
        success_count = sum(1 for v in results.values() if v is not None)
        logger.info(f"Scraped {success_count}/{len(urls)} URLs successfully")
        
        return results