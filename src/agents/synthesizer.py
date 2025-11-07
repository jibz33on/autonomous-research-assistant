"""Synthesizer agent - generates research reports."""

from typing import Dict, List
from src.llm.client import LLMClient
from src.llm.prompts import SYNTHESIZER_SYSTEM_PROMPT, SYNTHESIZER_USER_TEMPLATE
from src.llm.prompts import QA_SYSTEM_PROMPT, QA_USER_TEMPLATE
from src.rag.retriever import Retriever
from src.utils.config import settings
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


class SynthesizerAgent:
    """Synthesizes research documents into comprehensive reports."""
    
    def __init__(self):
        """Initialize LLM client and retriever."""
        self.llm = LLMClient(temperature=settings.temperature_synthesizer)
        self.retriever = Retriever()
        logger.info("SynthesizerAgent initialized")
    
    def synthesize_report(
        self, 
        topic: str, 
        documents: List[Dict], 
        session_id: str
    ) -> Dict:
        """
        Synthesize documents into a research report.
        
        Args:
            topic: Research topic
            documents: List of documents from executor
            session_id: Unique session ID for RAG storage
            
        Returns:
            Dict with:
            - report: str - Formatted research report
            - sources: List[str] - List of source URLs
        """
        try:
            logger.info(f"Synthesizing report for: '{topic}' ({len(documents)} documents)")
            
            # Step 1: Store documents in RAG
            self.retriever.store_documents(documents, session_id)
            
            # Step 2: Retrieve relevant chunks
            relevant_chunks = self.retriever.retrieve(
                query=topic,
                session_id=session_id,
                top_k=settings.retrieval_top_k
            )
            
            # Step 3: Format context with citations
            context = self._format_context_with_citations(relevant_chunks, documents)
            
            # Step 4: Generate report
            user_message = SYNTHESIZER_USER_TEMPLATE.format(
                topic=topic,
                context=context
            )
            
            report = self.llm.invoke(
                system_prompt=SYNTHESIZER_SYSTEM_PROMPT,
                user_message=user_message
            )
            
            # Step 5: Extract unique sources
            sources = list(set([doc['url'] for doc in documents]))
            
            logger.info(f"Report generated: {len(report)} chars, {len(sources)} sources")
            
            return {
                'report': report,
                'sources': sources
            }
            
        except Exception as e:
            logger.error(f"Failed to synthesize report: {e}")
            raise
    
    def answer_question(self, question: str, session_id: str) -> str:
        """
        Answer a question using stored research.
        
        Args:
            question: User question
            session_id: Session ID with stored documents
            
        Returns:
            Answer with citations
        """
        try:
            logger.info(f"Answering question: '{question}'")
            
            # Retrieve relevant chunks
            relevant_chunks = self.retriever.retrieve(
                query=question,
                session_id=session_id,
                top_k=5
            )
            
            # Format context
            context = "\n\n".join([
                f"[{i+1}] {chunk}" 
                for i, chunk in enumerate(relevant_chunks)
            ])
            
            # Generate answer
            user_message = QA_USER_TEMPLATE.format(
                context=context,
                question=question
            )
            
            answer = self.llm.invoke(
                system_prompt=QA_SYSTEM_PROMPT,
                user_message=user_message
            )
            
            logger.info("Answer generated")
            return answer
            
        except Exception as e:
            logger.error(f"Failed to answer question: {e}")
            raise
    
    def _format_context_with_citations(
        self, 
        chunks: List[str], 
        documents: List[Dict]
    ) -> str:
        """
        Format chunks with source citations.
        
        Args:
            chunks: Retrieved text chunks
            documents: Original documents with URLs
            
        Returns:
            Formatted context string with [1], [2] citations
        """
        # Create URL to index mapping
        url_to_index = {doc['url']: i + 1 for i, doc in enumerate(documents)}
        
        # Format chunks (simplified - just number them)
        context_parts = []
        for i, chunk in enumerate(chunks):
            context_parts.append(f"[{i+1}] {chunk}")
        
        return "\n\n".join(context_parts)