"""Tavily web search tool."""
from typing import List, Dict, Optional
from tavily import TavilyClient
from ..utils.config import settings
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class TavilySearch:
    """Wrapper for Tavily search API."""
    
    def __init__(self):
        """Initialize Tavily client."""
        self.client = TavilyClient(api_key=settings.tavily_api_key)
        logger.info("Initialized Tavily search client")
    
    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict]:
        """
        Search the web using Tavily.
        
        Args:
            query: Search query string
            max_results: Maximum number of results (defaults to config)
            
        Returns:
            List of search results with keys: url, title, content, score
        """
        # TODO: Implement on weekend
        # 1. Use self.client.search() with query
        # 2. Set max_results from parameter or config
        # 3. Extract relevant fields from response
        # 4. Add error handling and logging
        # 5. Return formatted results
        # Example return format:
        # [
        #     {
        #         'url': 'https://example.com',
        #         'title': 'Example Title',
        #         'content': 'Snippet of content...',
        #         'score': 0.95
        #     }
        # ]
        pass