"""LLM client wrapper for OpenAI."""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List, Dict, Optional
from ..utils.config import settings
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class LLMClient:
    """Wrapper for OpenAI LLM with standard configurations."""
    
    def __init__(self, temperature: float = 0.7, model: Optional[str] = None):
        """
        Initialize LLM client.
        
        Args:
            temperature: Sampling temperature
            model: Model name (defaults to config)
        """
        self.model = model or settings.llm_model
        self.temperature = temperature
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_tokens=settings.max_tokens,
            openai_api_key=settings.openai_api_key
        )
        logger.info(f"Initialized LLM client with model: {self.model}")
    
    def invoke(self, system_prompt: str, user_message: str) -> str:
        """
        Invoke LLM with system and user messages.
        
        Args:
            system_prompt: System instruction
            user_message: User input
            
        Returns:
            LLM response as string
        """
        # TODO: Implement on weekend
        # 1. Create messages list with SystemMessage and HumanMessage
        # 2. Call self.llm.invoke(messages)
        # 3. Extract and return content
        # 4. Add error handling
        pass
    
    def invoke_with_json(self, system_prompt: str, user_message: str) -> Dict:
        """
        Invoke LLM and parse response as JSON.
        
        Args:
            system_prompt: System instruction
            user_message: User input
            
        Returns:
            Parsed JSON response as dict
        """
        # TODO: Implement on weekend
        # 1. Add JSON formatting instruction to system prompt
        # 2. Call invoke()
        # 3. Parse response as JSON
        # 4. Handle JSON parsing errors
        pass