"""Vector store management using ChromaDB."""
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from ..utils.config import settings
from ..utils.logging import setup_logger
from .embeddings import get_embedding_function

logger = setup_logger(__name__)

class VectorStore:
    """Manages ChromaDB vector store for document embeddings."""
    
    def __init__(self):
        """Initialize ChromaDB client."""
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.embedding_function = get_embedding_function()
        logger.info(f"Initialized vector store at {settings.chroma_persist_dir}")
    
    def create_collection(self, collection_name: str):
        """
        Create or get a collection.
        
        Args:
            collection_name: Name of the collection (use session_id)
            
        Returns:
            Collection object
        """
        # TODO: Implement on weekend
        # Use self.client.get_or_create_collection()
        # Pass collection_name and embedding_function
        pass
    
    def add_documents(self, collection_name: str, chunks: List[Dict]):
        """
        Add document chunks to collection.
        
        Args:
            collection_name: Collection name
            chunks: List of chunks with 'text' and 'metadata'
        """
        # TODO: Implement on weekend
        # 1. Get or create collection
        # 2. Prepare data: documents (texts), metadatas, ids
        # 3. Use collection.add() to insert
        # 4. Generate unique IDs for each chunk
        pass
    
    def query_collection(self, collection_name: str, query_text: str, top_k: Optional[int] = None) -> List[str]:
        """
        Query collection for relevant chunks.
        
        Args:
            collection_name: Collection name
            query_text: Query text
            top_k: Number of results (defaults to config)
            
        Returns:
            List of relevant text chunks
        """
        # TODO: Implement on weekend
        # 1. Get collection
        # 2. Use collection.query() with query_text
        # 3. Set n_results to top_k or config default
        # 4. Extract and return document texts
        pass
    
    def delete_collection(self, collection_name: str):
        """
        Delete a collection.
        
        Args:
            collection_name: Collection name to delete
        """
        # TODO: Implement on weekend
        # Use self.client.delete_collection()
        pass