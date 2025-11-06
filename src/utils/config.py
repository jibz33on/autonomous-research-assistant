"""Configuration management using Pydantic settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    openai_api_key: str = Field(..., description="OpenAI API key")
    tavily_api_key: str = Field(..., description="Tavily API key")
    
    # LLM Settings
    llm_model: str = Field(default='gpt-4o-mini', description="OpenAI model name")
    temperature_planner: float = Field(default=0.3, description="Temperature for planner agent")
    temperature_synthesizer: float = Field(default=0.7, description="Temperature for synthesizer agent")
    max_tokens: int = Field(default=2000, description="Max tokens for LLM responses")
    
    # Search Settings
    max_search_results: int = Field(default=3, description="Max results per search query")
    max_sources_per_query: int = Field(default=3, description="Max sources to scrape per query")
    search_timeout: int = Field(default=30, description="Search timeout in seconds")
    
    # RAG Settings
    chunk_size: int = Field(default=1000, description="Text chunk size for embeddings")
    chunk_overlap: int = Field(default=200, description="Overlap between chunks")
    retrieval_top_k: int = Field(default=10, description="Number of chunks to retrieve")
    embedding_model: str = Field(default="text-embedding-3-small", description="OpenAI embedding model")
    
    # Paths
    chroma_persist_dir: str = Field(default='./data/chroma_db', description="Chroma DB persistence directory")
    
    # Application Settings
    max_iterations: int = Field(default=3, description="Max iterations for research loop")
    enable_caching: bool = Field(default=True, description="Enable result caching")
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )

# Global settings instance
settings = Settings()