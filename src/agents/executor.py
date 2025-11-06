"""Executor Agent - Searches and collects documents."""
from typing import List, Dict
from ..tools.websearch import TavilySearch
from ..tools.scraper import WebScraper
from ..utils.config import settings
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class ExecutorAgent:
    """Agent that executes searches and collects information."""
    
    def __init__(self):
        """Initialize executor with search and scraping tools."""
        self.search_tool = TavilySearch()
        self.scraper = WebScraper()
        logger.info("Initialized Executor Agent")
    
    def execute_research(self, queries: List[str]) -> List[Dict]:
        """
        Execute search queries and collect documents.
        
        Args:
            queries: List of search queries from planner
            
        Returns:
            List of document dicts with keys: url, title, content, source
        """
        # TODO: Implement on weekend
        # 1. For each query in queries:
        #    a. Search using self.search_tool.search(query)
        #    b. Take top N results (from config)
        #    c. For each result, scrape the URL
        #    d. Create document dict with metadata
        # 2. Collect all documents in a list
        # 3. Filter out failed scrapes (None content)
        # 4. Log statistics (queries executed, docs collected)
        # 5. Return list of documents
        # Document format:
        # {
        #     'url': '...',
        #     'title': '...',
        #     'content': '...',
        #     'source': 'web',
        #     'query': '...'  # which query found this
        # }
        pass