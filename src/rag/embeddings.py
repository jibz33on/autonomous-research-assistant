"""Embedding function for ChromaDB."""

from openai import OpenAI
from chromadb.api.types import EmbeddingFunction, Documents
from typing import List
from src.utils.config import settings
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


class CustomOpenAIEmbedding(EmbeddingFunction):
    """Custom embedding function using new OpenAI API (>=1.0.0)."""
    
    def __init__(self, api_key: str, model: str):
        """
        Initialize with OpenAI client.
        
        Args:
            api_key: OpenAI API key
            model: Embedding model name
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        logger.info(f"Custom embedding function created with model: {model}")
    
    def __call__(self, input: Documents) -> List[List[float]]:
        """
        Generate embeddings for input texts.
        
        Args:
            input: List of text strings
            
        Returns:
            List of embedding vectors
        """
        # Call new OpenAI API
        response = self.client.embeddings.create(
            input=input,
            model=self.model
        )
        
        # Extract embeddings
        embeddings = [item.embedding for item in response.data]
        return embeddings


def get_embedding_function():
    """
    Get OpenAI embedding function for ChromaDB.
    
    Returns:
        Custom OpenAI embedding function compatible with new API
    """
    logger.info(f"Creating embedding function with model: {settings.embedding_model}")
    
    embedding_fn = CustomOpenAIEmbedding(
        api_key=settings.openai_api_key,
        model=settings.embedding_model
    )
    
    return embedding_fn