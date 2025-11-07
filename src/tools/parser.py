"""Document parsing utilities."""
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.utils.config import settings
from src.utils.logging import setup_logger

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
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Format as list of dicts with metadata
        result = []
        for i, chunk in enumerate(chunks):
            result.append({
                'text': chunk,
                'metadata': {
                    **metadata,  # Include original metadata
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                }
            })
        
        logger.info(f"Chunked document into {len(chunks)} pieces")
        return result
    
    def chunk_multiple_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Chunk multiple documents.
        
        Args:
            documents: List of documents with 'content' and metadata
            
        Returns:
            List of all chunks from all documents
        """
        all_chunks = []
        
        for doc in documents:
            text = doc.get('content', '')
            if not text:
                logger.warning(f"Skipping document with no content: {doc.get('url', 'unknown')}")
                continue
            
            # Extract metadata (everything except 'content')
            metadata = {k: v for k, v in doc.items() if k != 'content'}
            
            # Chunk this document
            chunks = self.chunk_document(text, metadata)
            all_chunks.extend(chunks)
        
        logger.info(f"Chunked {len(documents)} documents into {len(all_chunks)} total chunks")
        return all_chunks