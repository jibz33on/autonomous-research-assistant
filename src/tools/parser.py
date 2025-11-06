"""Document parsing utilities."""
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..utils.config import settings
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class DocumentParser:
    """Parses and chunks documents for RAG."""
    
    def __init__(self):
        """Initialize document parser with text splitter."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        logger.info(f"Initialized document parser (chunk_size={settings.chunk_size})")
    
    def chunk_document(self, text: str, metadata: Dict) -> List[Dict]:
        """
        Chunk a document into smaller pieces for embedding.
        
        Args:
            text: Document text content
            metadata: Document metadata (url, title, etc.)
            
        Returns:
            List of chunks with metadata
        """
        # TODO: Implement on weekend
        # 1. Use self.text_splitter.split_text(text)
        # 2. Create list of dicts with chunk text + metadata
        # 3. Add chunk index to each chunk's metadata
        # Format: [{'text': '...', 'metadata': {...}}, ...]
        pass
    
    def chunk_multiple_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Chunk multiple documents.
        
        Args:
            documents: List of documents with 'content' and metadata
            
        Returns:
            List of all chunks from all documents
        """
        # TODO: Implement on weekend
        # Loop through documents and call chunk_document for each
        # Combine all chunks into single list
        pass