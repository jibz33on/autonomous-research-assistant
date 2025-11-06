"""Planner Agent - Breaks down research topic."""
from typing import Dict
from ..llm.client import LLMClient
from ..llm.prompts import PLANNER_SYSTEM_PROMPT, PLANNER_USER_TEMPLATE
from ..utils.config import settings
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class PlannerAgent:
    """Agent that plans the research strategy."""
    
    def __init__(self):
        """Initialize planner with LLM client."""
        self.llm = LLMClient(temperature=settings.temperature_planner)
        logger.info("Initialized Planner Agent")
    
    def create_plan(self, topic: str) -> Dict:
        """
        Create research plan with subtopics and search queries.
        
        Args:
            topic: Research topic provided by user
            
        Returns:
            dict with 'subtopics' and 'search_queries'
        """
        # TODO: Implement on weekend
        # 1. Format user message with PLANNER_USER_TEMPLATE
        # 2. Call self.llm.invoke_with_json() with system prompt and user message
        # 3. Validate response has required keys
        # 4. Log the plan
        # 5. Return the plan dict
        pass