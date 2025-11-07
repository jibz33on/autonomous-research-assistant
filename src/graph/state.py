"""
LangGraph State Definition
Defines the data structure that flows through the research workflow.
"""

from typing import TypedDict, List, Dict, Annotated
import operator


class ResearchState(TypedDict):
    """
    State schema for the research workflow.
    
    Fields are accumulated/updated as the workflow progresses through nodes.
    Using Annotated with operator.add for fields that should accumulate.
    """
    
    # INPUT - User provides
    topic: str  # The research topic
    
    # PLANNER OUTPUTS
    subtopics: List[str]  # Key areas identified for research
    search_queries: List[str]  # Specific queries to execute
    
    # EXECUTOR OUTPUTS
    # Using Annotated with operator.add to accumulate documents across iterations
    documents: Annotated[List[Dict], operator.add]  # Collected documents with metadata
    
    # RAG SESSION
    session_id: str  # Unique ID for vector store collection
    
    # SYNTHESIZER OUTPUTS
    report: str  # Final research report
    sources: List[str]  # List of source URLs used
    
    # METADATA
    status: str  # Current workflow status
    logs: Annotated[List[str], operator.add]  # Activity log (accumulates)
    error: str  # Error message if something fails