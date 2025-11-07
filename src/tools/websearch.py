"""Tavily web search tool."""
from typing import List, Dict, Optional
from tavily import TavilyClient
from src.utils.config import settings
from src.utils.logging import setup_logger

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
        try:
            # Use config default if max_results not provided
            max_results = max_results or settings.max_search_results
            
            logger.info(f"Searching: '{query}' (max_results={max_results})")
            
            # Call Tavily API
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="basic"
            )
            
            # Extract results
            results = response.get('results', [])
            logger.info(f"Found {len(results)} results")
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed for '{query}': {str(e)}")
            return []