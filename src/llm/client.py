"""LLM client wrapper for OpenAI."""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List, Dict, Optional
import json
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
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"LLM invocation failed: {str(e)}")
            raise
    
    def invoke_with_json(self, system_prompt: str, user_message: str) -> Dict:
        """
        Invoke LLM and parse response as JSON.
        
        Args:
            system_prompt: System instruction
            user_message: User input
            
        Returns:
            Parsed JSON response as dict
        """
        try:
            # Add JSON instruction to system prompt
            json_system_prompt = system_prompt + "\n\nYou must respond with valid JSON only."
            
            messages = [
                SystemMessage(content=json_system_prompt),
                HumanMessage(content=user_message)
            ]
            response = self.llm.invoke(messages)
            
            # Parse JSON response
            return json.loads(response.content)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.error(f"Response was: {response.content}")
            raise
        except Exception as e:
            logger.error(f"LLM JSON invocation failed: {str(e)}")
            raise