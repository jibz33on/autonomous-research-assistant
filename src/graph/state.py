"""State schema for LangGraph workflow."""
from typing import TypedDict, List, Dict, Annotated
import operator

class ResearchState(TypedDict):
    """State that flows through the research workflow."""
    
    # Input
    topic: str
    
    # Planner outputs
    subtopics: List[str]
    search_queries: List[str]
    
    # Executor outputs
    documents: Annotated[List[Dict], operator.add]  # Accumulate documents
    
    # RAG
    session_id: str
    
    # Synthesizer outputs
    report: str
    sources: List[str]
    
    # Metadata
    status: str
    logs: Annotated[List[str], operator.add]  # Accumulate logs
    error: str  # Store any errors