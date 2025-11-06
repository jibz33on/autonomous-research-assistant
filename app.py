"""Streamlit UI for Autonomous Research Assistant."""
import streamlit as st
from dotenv import load_dotenv
import uuid
from src.graph.workflow import build_research_graph
from src.agents.synthesizer import SynthesizerAgent
from src.utils.logging import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)

# Page config
st.set_page_config(
    page_title="Autonomous Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'research_complete' not in st.session_state:
    st.session_state.research_complete = False
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'report' not in st.session_state:
    st.session_state.report = None
if 'sources' not in st.session_state:
    st.session_state.sources = []

# Title and description
st.title("🔍 Autonomous Research Assistant")
st.markdown("*Powered by LangGraph, RAG, and GPT-4*")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📚 About")
    st.markdown("""
    This agentic system autonomously:
    - 📋 Plans research strategy
    - 🔎 Searches and collects information
    - 📝 Synthesizes findings into a report
    - 💬 Answers follow-up questions
    
    **Tech Stack:**
    - LangGraph + LangChain
    - OpenAI GPT-4o-mini
    - Tavily Search API
    - ChromaDB + RAG
    """)
    
    st.markdown("---")
    st.markdown("**Example Topics:**")
    st.markdown("- Impact of AI on healthcare")
    st.markdown("- Zero-shot RL for robotics")
    st.markdown("- Quantum computing applications")
    st.markdown("- Climate change solutions")

# Main interface
col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input(
        "Enter research topic:",
        placeholder="e.g., Recent developments in quantum computing",
        key="topic_input"
    )

with col2:
    st.write("")  # Spacing
    st.write("")  # Spacing
    research_button = st.button("🚀 Start Research", type="primary", use_container_width=True)

# Research execution
if research_button:
    if not topic:
        st.error("⚠️ Please enter a research topic")
    else:
        # TODO: Implement on weekend
        # 1. Show progress bar and status updates
        # 2. Build graph: graph = build_research_graph()
        # 3. Initialize state with topic
        # 4. Invoke graph and stream results
        # 5. Display logs in real-time
        # 6. Store results in session state
        # 7. Set research_complete = True
        
        st.info("🚧 This will be implemented on the weekend!")
        st.markdown("**What will happen:**")
        st.markdown("1. 📋 Planner breaks down your topic")
        st.markdown("2. 🔎 Executor searches and collects documents")
        st.markdown("3. 📝 Synthesizer creates a comprehensive report")

# Display report if research is complete
if st.session_state.research_complete and st.session_state.report:
    st.markdown("---")
    st.subheader("📄 Research Report")
    
    # Display report
    st.markdown(st.session_state.report)
    
    # Display sources
    with st.expander("📚 View Sources"):
        for idx, source in enumerate(st.session_state.sources, 1):
            st.markdown(f"**[{idx}]** {source}")
    
    # Download button
    st.download_button(
        label="⬇️ Download Report",
        data=st.session_state.report,
        file_name=f"research_report_{st.session_state.session_id}.md",
        mime="text/markdown"
    )

# Q&A Section
st.markdown("---")
st.subheader("💬 Ask Follow-up Questions")

if st.session_state.research_complete:
    question = st.text_input(
        "Ask a question about the research:",
        placeholder="e.g., What are the main challenges mentioned?",
        key="question_input"
    )
    
    if st.button("Ask", type="secondary"):
        if question:
            # TODO: Implement on weekend
            # 1. Initialize SynthesizerAgent
            # 2. Call answer_question() with question and session_id
            # 3. Display answer
            st.info("🚧 Q&A will be implemented on the weekend!")
        else:
            st.warning("Please enter a question")
else:
    st.info("ℹ️ Complete a research task first to enable Q&A")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center'>Built for Educosys Hackathon 2025 | "
    "Powered by LangGraph & OpenAI</div>",
    unsafe_allow_html=True
)