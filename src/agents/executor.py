"""Executor agent - collects research documents."""

from typing import List, Dict
from src.tools.websearch import TavilySearch
from src.tools.scraper import WebScraper
from src.utils.config import settings
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


class ExecutorAgent:
    """Executes research plan by collecting documents."""
    
    def __init__(self):
        """Initialize search and scraper tools."""
        self.search = TavilySearch()
        self.scraper = WebScraper()
        logger.info("ExecutorAgent initialized")
    
    def execute_research(self, queries: List[str]) -> List[Dict]:
        """
        Execute research by searching and scraping documents.
        
        Args:
            queries: List of search queries
            
        Returns:
            List of documents with content and metadata
        """
        try:
            logger.info(f"Executing research with {len(queries)} queries")
            
            all_documents = []
            
            for query in queries:
                logger.info(f"Processing query: '{query}'")
                
                # Step 1: Search
                search_results = self.search.search(query)
                
                if not search_results:
                    logger.warning(f"No results for query: '{query}'")
                    continue
                
                # Step 2: Get URLs to scrape (limit per query)
                urls_to_scrape = [
                    r['url'] for r in search_results[:settings.max_sources_per_query]
                ]
                
                # Step 3: Scrape URLs
                scraped_content = self.scraper.scrape_multiple(urls_to_scrape)
                
                # Step 4: Build documents
                for result in search_results[:settings.max_sources_per_query]:
                    url = result['url']
                    content = scraped_content.get(url)
                    
                    # Only add if scraping succeeded
                    if content:
                        document = {
                            'url': url,
                            'title': result['title'],
                            'content': content,
                            'source': 'web',
                            'query': query
                        }
                        all_documents.append(document)
                
                logger.info(f"Collected {len([d for d in all_documents if d['query'] == query])} "
                           f"documents for query: '{query}'")
            
            logger.info(f"Total documents collected: {len(all_documents)}")
            return all_documents
            
        except Exception as e:
            logger.error(f"Failed to execute research: {e}")
            raise