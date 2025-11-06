"""Synthesizer Agent - Creates research report."""
from typing import List, Dict
from ..llm.client import LLMClient
from ..llm.prompts import SYNTHESIZER_SYSTEM_PROMPT, SYNTHESIZER_USER_TEMPLATE
from ..rag.retriever import Retriever
from ..utils.config import settings
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class SynthesizerAgent:
    """Agent that synthesizes documents into a research report."""
    
    def __init__(self):
        """Initialize synthesizer with LLM and retriever."""
        self.llm = LLMClient(temperature=settings.temperature_synthesizer)
        self.retriever = Retriever()
        logger.info("Initialized Synthesizer Agent")
    
    def synthesize_report(self, topic: str, documents: List[Dict], session_id: str) -> Dict:
        """
        Generate research report from collected documents.
        
        Args:
            topic: Original research topic
            documents: List of collected documents
            session_id: Vector store session ID
            
        Returns:
            dict with 'report' and 'sources'
        """
        # TODO: Implement on weekend
        # 1. Store documents in RAG using self.retriever.store_documents()
        # 2. Retrieve most relevant chunks using self.retriever.retrieve()
        # 3. Format chunks into context string with source numbers
        # 4. Format user message with SYNTHESIZER_USER_TEMPLATE
        # 5. Call self.llm.invoke() with system and user prompts
        # 6. Extract citations from documents
        # 7. Return dict with 'report' and 'sources' list
        pass
    
    def answer_question(self, question: str, session_id: str) -> str:
        """
        Answer a question using RAG.
        
        Args:
            question: User's question
            session_id: Vector store session ID
            
        Returns:
            Answer string with citations
        """
        # TODO: Implement on weekend
        # 1. Retrieve relevant chunks for question
        # 2. Format QA prompt with context
        # 3. Call LLM
        # 4. Return answer
        pass