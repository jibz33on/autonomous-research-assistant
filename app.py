"""
Autonomous Research Assistant - Streamlit UI
A powerful AI-powered research tool using GPT-4, LangGraph, and RAG
"""

import streamlit as st
from datetime import datetime
import time
from src.graph.workflow import build_research_graph
from src.agents.synthesizer import SynthesizerAgent
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="Autonomous Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .example-topic {
        background: #f0f2f6;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        display: inline-block;
        cursor: pointer;
        transition: all 0.3s;
    }
    .example-topic:hover {
        background: #667eea;
        color: white;
    }
    .activity-log {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        max-height: 300px;
        overflow-y: auto;
        font-family: monospace;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'research_complete' not in st.session_state:
    st.session_state.research_complete = False
if 'report' not in st.session_state:
    st.session_state.report = ""
if 'sources' not in st.session_state:
    st.session_state.sources = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = ""
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'documents_count' not in st.session_state:
    st.session_state.documents_count = 0
if 'subtopics' not in st.session_state:
    st.session_state.subtopics = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# Sidebar
with st.sidebar:
    st.markdown("## 📚 About")
    st.info("""
    **Autonomous Research Assistant** uses cutting-edge AI to conduct 
    comprehensive research on any topic.
    
    It autonomously:
    - 🎯 Plans research strategy
    - 🔍 Searches and collects data
    - 📝 Synthesizes comprehensive reports
    - 💬 Answers follow-up questions
    """)
    
    st.markdown("## 🛠️ Tech Stack")
    st.markdown("""
    - **LLM**: GPT-4o-mini (OpenAI)
    - **Orchestration**: LangGraph
    - **Search**: Tavily API
    - **RAG**: ChromaDB + OpenAI Embeddings
    - **Framework**: Streamlit
    """)
    
    if st.session_state.research_complete:
        st.markdown("## 📊 Statistics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Documents", st.session_state.documents_count)
            st.metric("Sources", len(st.session_state.sources))
        with col2:
            st.metric("Subtopics", len(st.session_state.subtopics))
            if st.session_state.start_time:
                elapsed = int(time.time() - st.session_state.start_time)
                st.metric("Time", f"{elapsed}s")
    
    st.markdown("## 💡 Tips")
    st.markdown("""
    - Be specific with your topic
    - Ask follow-up questions after research
    - Download report for offline use
    """)

# Main header
st.markdown('<h1 class="main-header">🔬 Autonomous Research Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Powered by GPT-4, LangGraph & RAG</p>', unsafe_allow_html=True)

# New Search button (shown when research is complete)
if st.session_state.research_complete:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Start New Research", type="primary", use_container_width=True):
            # Reset session state
            st.session_state.research_complete = False
            st.session_state.report = ""
            st.session_state.sources = []
            st.session_state.session_id = ""
            st.session_state.logs = []
            st.session_state.documents_count = 0
            st.session_state.subtopics = []
            st.session_state.start_time = None
            if 'selected_topic' in st.session_state:
                del st.session_state.selected_topic
            st.rerun()

# Only show input section if research not complete
if not st.session_state.research_complete:
    # Input Section
    st.markdown("### 🎯 What would you like to research?")

    # Example topics
    st.markdown("**Quick Examples:**")
    col1, col2, col3 = st.columns(3)
    example_topics = [
        "Impact of AI on education",
        "Climate change solutions 2024",
        "Quantum computing applications",
        "Future of renewable energy",
        "Blockchain in healthcare",
        "Space exploration technologies"
    ]

    for i, topic in enumerate(example_topics):
        with [col1, col2, col3][i % 3]:
            if st.button(topic, key=f"example_{i}", use_container_width=True):
                st.session_state.selected_topic = topic

    # Main input
    topic = st.text_input(
        "Enter your research topic:",
        value=st.session_state.get('selected_topic', ''),
        placeholder="e.g., Recent advances in artificial intelligence",
        help="Be specific for better results",
        label_visibility="collapsed"
    )

    # Research button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        research_button = st.button(
            "🚀 Start Research",
            type="primary",
            use_container_width=True,
            disabled=not topic or len(topic.strip()) < 10
        )

    if len(topic.strip()) > 0 and len(topic.strip()) < 10:
        st.warning("⚠️ Please enter a more detailed topic (at least 10 characters)")

    st.divider()

    # Execute Research
    if research_button and topic:
        st.session_state.start_time = time.time()
        st.session_state.research_complete = False
        st.session_state.logs = []
        
        # Progress section
        st.markdown("### 🔄 Research in Progress")
        
        progress_bar = st.progress(0)
        status_placeholder = st.empty()
        logs_placeholder = st.empty()
        
        try:
            # Build graph
            status_placeholder.info("🔧 Initializing research workflow...")
            progress_bar.progress(5)
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
            
            # Execute workflow with progress updates
            status_placeholder.info("🎯 Planning research strategy...")
            progress_bar.progress(15)
            time.sleep(0.5)
            
            # Stream through workflow
            final_state = None
            for state_update in graph.stream(initial_state):
                # LangGraph stream returns dict with node_name: state_updates
                for node_name, node_output in state_update.items():
                    
                    # Check if this node output has status
                    if isinstance(node_output, dict) and 'status' in node_output:
                        status = node_output['status']
                        
                        if status == 'planning_complete':
                            status_placeholder.success("✓ Research plan created!")
                            progress_bar.progress(35)
                            if 'logs' in node_output:
                                st.session_state.logs.extend(node_output['logs'])
                        
                        elif status == 'research_complete':
                            status_placeholder.success("✓ Documents collected!")
                            progress_bar.progress(70)
                            if 'logs' in node_output:
                                st.session_state.logs.extend(node_output['logs'])
                            if 'documents' in node_output:
                                st.session_state.documents_count = len(node_output['documents'])
                        
                        elif status == 'complete':
                            status_placeholder.success("✓ Report generated!")
                            progress_bar.progress(100)
                            if 'logs' in node_output:
                                st.session_state.logs.extend(node_output['logs'])
                            # Store the complete state
                            final_state = node_output
                    
                    # Display logs after each node
                    if st.session_state.logs:
                        logs_html = "<div class='activity-log'>"
                        for log in st.session_state.logs:
                            logs_html += f"<div>{log}</div>"
                        logs_html += "</div>"
                        logs_placeholder.markdown(logs_html, unsafe_allow_html=True)
                    
                    # Force Streamlit to update the UI
                    time.sleep(0.1)
            
            # Get final state if not captured during streaming
            if not final_state:
                final_state = graph.invoke(initial_state)
            
            # Store results
            st.session_state.report = final_state.get('report', '')
            st.session_state.sources = final_state.get('sources', [])
            st.session_state.session_id = final_state.get('session_id', '')
            st.session_state.subtopics = final_state.get('subtopics', [])
            st.session_state.research_complete = True
            
            time.sleep(0.5)
            status_placeholder.success("✅ Research Complete!")
            st.balloons()
            st.rerun()
            
        except Exception as e:
            logger.error(f"Research failed: {str(e)}")
            st.error(f"❌ Research failed: {str(e)}")
            st.stop()

# Display Results
if st.session_state.research_complete and st.session_state.report:
    st.divider()
    
    # Results header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 📄 Research Report")
    with col2:
        st.download_button(
            label="⬇️ Download Report",
            data=st.session_state.report,
            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    # Display report
    st.markdown(st.session_state.report)
    
    # Expandable sections
    with st.expander("📋 Research Subtopics", expanded=False):
        for i, subtopic in enumerate(st.session_state.subtopics, 1):
            st.markdown(f"{i}. {subtopic}")
    
    with st.expander("🔗 Sources", expanded=False):
        for i, source in enumerate(st.session_state.sources, 1):
            st.markdown(f"{i}. [{source}]({source})")
    
    with st.expander("📊 Activity Log", expanded=False):
        for log in st.session_state.logs:
            st.text(log)
    
    st.divider()
    
    # Q&A Section
    st.markdown("### 💬 Ask Follow-Up Questions")
    st.info("Ask questions about the research above. The AI will answer using the collected documents.")
    
    question = st.text_input(
        "Your question:",
        placeholder="e.g., What are the main challenges?",
        key="qa_question"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        ask_button = st.button(
            "🤔 Get Answer",
            type="secondary",
            use_container_width=True,
            disabled=not question
        )
    
    if ask_button and question:
        with st.spinner("Analyzing documents..."):
            try:
                synthesizer = SynthesizerAgent()
                answer = synthesizer.answer_question(
                    question=question,
                    session_id=st.session_state.session_id
                )
                
                st.markdown("#### Answer:")
                st.success(answer)
                
            except Exception as e:
                logger.error(f"Q&A failed: {str(e)}")
                st.error(f"❌ Failed to answer question: {str(e)}")
    
    # Back to top button at the bottom
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⬆️ Back to Top - New Search", type="primary", use_container_width=True):
            # Reset and scroll to top
            st.session_state.research_complete = False
            st.session_state.report = ""
            st.session_state.sources = []
            st.session_state.session_id = ""
            st.session_state.logs = []
            st.session_state.documents_count = 0
            st.session_state.subtopics = []
            st.session_state.start_time = None
            if 'selected_topic' in st.session_state:
                del st.session_state.selected_topic
            st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Built by <b>Jibin Kunjumon</b></p>
    <p style='font-size: 0.9rem;'>🚀 Autonomous Research • 🧠 AI-Powered • 📚 RAG-Enhanced</p>
</div>
""", unsafe_allow_html=True)