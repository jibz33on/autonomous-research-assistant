"""
LangGraph Workflow Definition
Orchestrates the autonomous research workflow using LangGraph.
"""

from langgraph.graph import StateGraph, END
from src.graph.state import ResearchState
from src.graph.nodes import planner_node, executor_node, synthesizer_node
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def build_research_graph():
    """
    Builds the research workflow graph.
    
    Workflow:
    1. Planner Node: Analyzes topic → generates search queries
    2. Executor Node: Executes queries → collects documents  
    3. Synthesizer Node: Synthesizes documents → generates report
    
    Returns:
        Compiled LangGraph that can be invoked with initial state
    """
    logger.info("Building research workflow graph")
    
    # Create state graph with ResearchState schema
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("synthesizer", synthesizer_node)
    
    # Define edges (workflow flow)
    workflow.set_entry_point("planner")  # Start with planner
    workflow.add_edge("planner", "executor")  # planner → executor
    workflow.add_edge("executor", "synthesizer")  # executor → synthesizer
    workflow.add_edge("synthesizer", END)  # synthesizer → done
    
    logger.info("Workflow graph built successfully")
    logger.info("Flow: START → Planner → Executor → Synthesizer → END")
    
    # Compile and return
    return workflow.compile()


def run_research(topic: str) -> ResearchState:
    """
    Convenience function to run research workflow.
    
    Args:
        topic: Research topic to investigate
        
    Returns:
        Final state with report and sources
    """
    logger.info(f"Starting research workflow for topic: {topic}")
    
    # Build graph
    graph = build_research_graph()
    
    # Initialize state
    initial_state = {
        'topic': topic,
        'documents': [],
        'logs': [],
        'subtopics': [],
        'search_queries': [],
        'session_id': '',
        'report': '',
        'sources': [],
        'status': 'initialized',
        'error': ''
    }
    
    # Execute workflow
    logger.info("Executing workflow...")
    final_state = graph.invoke(initial_state)
    
    logger.info(f"Workflow completed with status: {final_state['status']}")
    
    return final_state


# Example usage
if __name__ == "__main__":
    # Test the workflow
    result = run_research("Impact of artificial intelligence on healthcare")
    
    print("\n" + "="*80)
    print("RESEARCH COMPLETE")
    print("="*80)
    print(f"\nStatus: {result['status']}")
    print(f"\nSubtopics: {result['subtopics']}")
    print(f"\nDocuments collected: {len(result['documents'])}")
    print(f"\nSources: {len(result['sources'])}")
    print(f"\n{result['report'][:500]}...")

    