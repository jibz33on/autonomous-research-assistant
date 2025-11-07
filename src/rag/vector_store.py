"""Vector store using ChromaDB for document embeddings."""

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Optional
from src.rag.embeddings import get_embedding_function
from src.utils.config import settings
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


class VectorStore:
    """Manages ChromaDB vector store for document retrieval."""
    
    def __init__(self):
        """Initialize ChromaDB client with persistent storage."""
        # Create ChromaDB client (auto-creates directory if needed)
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Get embedding function
        self.embedding_function = get_embedding_function()
        
        logger.info(f"VectorStore initialized: {settings.chroma_persist_dir}")
    
    def create_collection(self, collection_name: str) -> None:
        """
        Create a new collection (or get existing one).
        
        Args:
            collection_name: Unique name for this collection (e.g., session_id)
        """
        try:
            self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            logger.info(f"Collection created/loaded: {collection_name}")
        except Exception as e:
            logger.error(f"Failed to create collection {collection_name}: {e}")
            raise
    
    def add_documents(self, collection_name: str, chunks: List[Dict]) -> None:
        """
        Add document chunks to a collection.
        
        Args:
            collection_name: Collection to add to
            chunks: List of dicts with 'text' and 'metadata' keys
        """
        try:
            collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            
            # Extract texts and metadata
            texts = [chunk['text'] for chunk in chunks]
            metadatas = [chunk['metadata'] for chunk in chunks]
            
            # Generate unique IDs
            ids = [f"{collection_name}_{i}" for i in range(len(chunks))]
            
            # Add to collection (ChromaDB auto-generates embeddings)
            collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(chunks)} chunks to collection {collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to add documents to {collection_name}: {e}")
            raise
    
    def query_collection(
        self, 
        collection_name: str, 
        query: str, 
        top_k: int = 10
    ) -> List[str]:
        """
        Query collection for similar documents.
        
        Args:
            collection_name: Collection to query
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant text chunks
        """
        try:
            collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            
            # Query (ChromaDB auto-generates embedding for query)
            results = collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            # Extract documents (first query result)
            documents = results['documents'][0] if results['documents'] else []
            
            logger.info(f"Retrieved {len(documents)} chunks for query: '{query[:50]}...'")
            
            return documents
            
        except Exception as e:
            logger.error(f"Failed to query collection {collection_name}: {e}")
            raise
    
    def delete_collection(self, collection_name: str) -> None:
        """
        Delete a collection.
        
        Args:
            collection_name: Collection to delete
        """
        try:
            self.client.delete_collection(name=collection_name)
            logger.info(f"Deleted collection: {collection_name}")
        except Exception as e:
            logger.error(f"Failed to delete collection {collection_name}: {e}")
            raise
    
    def list_collections(self) -> List[str]:
        """
        List all collections.
        
        Returns:
            List of collection names
        """
        collections = self.client.list_collections()
        names = [c.name for c in collections]
        logger.info(f"Found {len(names)} collections")
        return names