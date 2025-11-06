"""Embedding generation utilities."""
from chromadb.utils import embedding_functions
from ..utils.config import settings
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

def get_embedding_function():
    """
    Get OpenAI embedding function for Chroma.
    
    Returns:
        ChromaDB embedding function configured for OpenAI
    """
    # TODO: Implement on weekend
    # Use chromadb.utils.embedding_functions.OpenAIEmbeddingFunction
    # Configure with:
    # - api_key from settings
    # - model_name from settings.embedding_model
    # Return the function object
    pass