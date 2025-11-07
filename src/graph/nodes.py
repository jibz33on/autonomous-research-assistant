"""
LangGraph Node Functions
Wraps agents as nodes that LangGraph can execute.
"""

from typing import Dict
import uuid
from src.agents.planner import PlannerAgent
from src.agents.executor import ExecutorAgent
from src.agents.synthesizer import SynthesizerAgent
from src.graph.state import ResearchState
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

# Initialize agents once (reused across invocations)
planner = PlannerAgent()
executor = ExecutorAgent()
synthesizer = SynthesizerAgent()


def planner_node(state: ResearchState) -> Dict:
    """
    Planner Node: Analyzes topic and creates research plan.
    
    Args:
        state: Current research state with 'topic'
        
    Returns:
        Dict with subtopics, search_queries, status, and logs
    """
    try:
        logger.info(f"=== PLANNER NODE: Analyzing topic '{state['topic']}' ===")
        
        topic = state['topic']
        plan = planner.create_plan(topic)
        
        logger.info(f"Generated {len(plan['subtopics'])} subtopics")
        logger.info(f"Generated {len(plan['search_queries'])} search queries")
        
        return {
            'subtopics': plan['subtopics'],
            'search_queries': plan['search_queries'],
            'status': 'planning_complete',
            'logs': [
                f"✓ Planner: Identified {len(plan['subtopics'])} key subtopics",
                f"✓ Planner: Generated {len(plan['search_queries'])} targeted search queries"
            ]
        }
        
    except Exception as e:
        logger.error(f"Planner node failed: {str(e)}")
        return {
            'status': 'error',
            'error': f"Planning failed: {str(e)}",
            'logs': [f"✗ Planner: Error - {str(e)}"]
        }


def executor_node(state: ResearchState) -> Dict:
    """
    Executor Node: Executes search queries and collects documents.
    
    Args:
        state: Current research state with 'search_queries'
        
    Returns:
        Dict with documents, status, and logs
    """
    try:
        logger.info("=== EXECUTOR NODE: Collecting research documents ===")
        
        queries = state['search_queries']
        logger.info(f"Executing {len(queries)} search queries")
        
        documents = executor.execute_research(queries)
        
        logger.info(f"Collected {len(documents)} documents")
        
        return {
            'documents': documents,  # Accumulated via operator.add
            'status': 'research_complete',
            'logs': [
                f"✓ Executor: Executed {len(queries)} search queries",
                f"✓ Executor: Collected {len(documents)} documents"
            ]
        }
        
    except Exception as e:
        logger.error(f"Executor node failed: {str(e)}")
        return {
            'status': 'error',
            'error': f"Research execution failed: {str(e)}",
            'logs': [f"✗ Executor: Error - {str(e)}"]
        }


def synthesizer_node(state: ResearchState) -> Dict:
    """
    Synthesizer Node: Creates research report from collected documents.
    
    Args:
        state: Current research state with 'topic' and 'documents'
        
    Returns:
        Dict with session_id, report, sources, status, and logs
    """
    try:
        logger.info("=== SYNTHESIZER NODE: Generating research report ===")
        
        topic = state['topic']
        documents = state['documents']
        
        # Generate or use existing session ID
        session_id = state.get('session_id') or str(uuid.uuid4())
        
        logger.info(f"Synthesizing {len(documents)} documents into report")
        
        result = synthesizer.synthesize_report(
            topic=topic,
            documents=documents,
            session_id=session_id
        )
        
        logger.info("Report generated successfully")
        logger.info(f"Used {len(result['sources'])} unique sources")
        
        return {
            'session_id': session_id,
            'report': result['report'],
            'sources': result['sources'],
            'status': 'complete',
            'logs': [
                f"✓ Synthesizer: Processed {len(documents)} documents",
                f"✓ Synthesizer: Generated comprehensive report",
                f"✓ Synthesizer: Cited {len(result['sources'])} sources"
            ]
        }
        
    except Exception as e:
        logger.error(f"Synthesizer node failed: {str(e)}")
        return {
            'status': 'error',
            'error': f"Synthesis failed: {str(e)}",
            'logs': [f"✗ Synthesizer: Error - {str(e)}"]
        }