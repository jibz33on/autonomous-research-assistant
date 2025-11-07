"""Planner agent - creates research strategy."""

from typing import Dict
from src.llm.client import LLMClient
from src.llm.prompts import PLANNER_SYSTEM_PROMPT, PLANNER_USER_TEMPLATE
from src.utils.config import settings
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


class PlannerAgent:
    """Analyzes research topics and creates strategic plans."""
    
    def __init__(self):
        """Initialize planner with LLM client."""
        self.llm = LLMClient(temperature=settings.temperature_planner)
        logger.info("PlannerAgent initialized")
    
    def create_plan(self, topic: str) -> Dict:
        """
        Create a research plan for the given topic.
        
        Args:
            topic: Research topic to analyze
            
        Returns:
            Dict with:
            - subtopics: List[str] - Key areas to research
            - search_queries: List[str] - Specific queries to execute
        """
        try:
            logger.info(f"Creating research plan for: '{topic}'")
            
            # Format user message
            user_message = PLANNER_USER_TEMPLATE.format(topic=topic)
            
            # Call LLM with JSON mode
            plan = self.llm.invoke_with_json(
                system_prompt=PLANNER_SYSTEM_PROMPT,
                user_message=user_message
            )
            
            # Validate response
            if 'subtopics' not in plan or 'search_queries' not in plan:
                raise ValueError("LLM response missing required fields")
            
            logger.info(f"Plan created: {len(plan['subtopics'])} subtopics, "
                       f"{len(plan['search_queries'])} queries")
            
            return plan
            
        except Exception as e:
            logger.error(f"Failed to create plan for '{topic}': {e}")
            raise