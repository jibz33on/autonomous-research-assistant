"""High-level retriever combining parsing and vector storage."""

from typing import List, Dict, Optional
from src.tools.parser import DocumentParser
from src.rag.vector_store import VectorStore
from src.utils.config import settings
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


class Retriever:
    """High-level interface for document storage and retrieval."""
    
    def __init__(self):
        """Initialize parser and vector store."""
        self.parser = DocumentParser()
        self.vector_store = VectorStore()
        logger.info("Retriever initialized")
    
    def store_documents(
        self, 
        documents: List[Dict], 
        session_id: str
    ) -> None:
        """
        Store documents in vector database.
        
        Handles the full pipeline: chunk → embed → store
        
        Args:
            documents: List of dicts with 'content' and metadata fields
            session_id: Unique session identifier for collection
        """
        try:
            logger.info(f"Storing {len(documents)} documents for session {session_id}")
            
            # Step 1: Chunk documents
            chunks = self.parser.chunk_multiple_documents(documents)
            logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
            
            # Step 2: Create collection
            self.vector_store.create_collection(session_id)
            
            # Step 3: Add chunks to vector store
            self.vector_store.add_documents(session_id, chunks)
            
            logger.info(f"Successfully stored documents for session {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to store documents: {e}")
            raise
    
    def retrieve(
        self, 
        query: str, 
        session_id: str, 
        top_k: Optional[int] = None
    ) -> List[str]:
        """
        Retrieve relevant chunks for a query.
        
        Args:
            query: Search query
            session_id: Session identifier
            top_k: Number of chunks to retrieve (defaults to config)
            
        Returns:
            List of relevant text chunks
        """
        try:
            top_k = top_k or settings.retrieval_top_k
            
            logger.info(f"Retrieving top {top_k} chunks for query: '{query[:50]}...'")
            
            # Query vector store
            chunks = self.vector_store.query_collection(
                collection_name=session_id,
                query=query,
                top_k=top_k
            )
            
            logger.info(f"Retrieved {len(chunks)} relevant chunks")
            
            return chunks
            
        except Exception as e:
            logger.error(f"Failed to retrieve chunks: {e}")
            raise
    
    def delete_session(self, session_id: str) -> None:
        """
        Delete a session's data.
        
        Args:
            session_id: Session identifier to delete
        """
        try:
            self.vector_store.delete_collection(session_id)
            logger.info(f"Deleted session: {session_id}")
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            raise