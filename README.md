# 🔬 Autonomous Research Assistant

An AI-powered research tool that autonomously plans, executes, and synthesizes comprehensive research reports on any topic.

## 📖 Description

The Autonomous Research Assistant uses cutting-edge AI technologies to conduct end-to-end research autonomously. It breaks down complex topics into subtopics, searches the web for relevant information, and synthesizes findings into a comprehensive report with citations.

## 🎯 Use Cases

- **Academic Research**: Quickly gather information on research topics
- **Market Analysis**: Understand industry trends and competitive landscapes
- **Learning & Education**: Deep-dive into new subjects efficiently
- **Content Creation**: Research background information for articles or reports
- **Decision Making**: Gather insights for informed business decisions

## 🌐 Scope

**What it does:**
- Autonomously plans research strategy by identifying key subtopics
- Executes web searches and collects relevant documents
- Synthesizes information into structured reports with citations
- Answers follow-up questions using collected research (RAG-powered)

**What it doesn't do:**
- Real-time data analysis or live monitoring
- Access to paywalled or authenticated content
- Generate original research or conduct experiments

## 🏗️ Architecture

![Architecture Diagram]
(./assets/architecture-diagram.png)

The system follows a layered architecture with 6 layers:
```
Layer 0: Foundation
├── Configuration management (config.py)
└── Logging utilities (logging.py)

Layer 1: LLM
├── OpenAI client wrapper (client.py)
└── System prompts (prompts.py)

Layer 2: Tools
├── Web search (websearch.py) - Tavily API
├── Web scraper (scraper.py) - BeautifulSoup
└── Document parser (parser.py) - Text chunking

Layer 3: RAG (Retrieval-Augmented Generation)
├── Embeddings (embeddings.py) - OpenAI text-embedding-3-small
├── Vector store (vector_store.py) - ChromaDB
└── Retriever (retriever.py) - Semantic search

Layer 4: Agents
├── Planner Agent - Creates research plan
├── Executor Agent - Collects documents
└── Synthesizer Agent - Generates report + Q&A

Layer 5: Graph (LangGraph Workflow)
├── State definition (state.py)
├── Node functions (nodes.py)
└── Workflow orchestration (workflow.py)

Layer 6: Application
└── Streamlit UI (app.py)
```

**Workflow:**
```
User Input → Planner Agent → Executor Agent → Synthesizer Agent → Report + Q&A
              (subtopics)      (documents)       (RAG synthesis)
```

## 🛠️ Tech Stack

- **LLM**: GPT-4o-mini (OpenAI)
- **Orchestration**: LangGraph
- **Web Search**: Tavily API
- **Web Scraping**: BeautifulSoup4, Requests
- **RAG**: ChromaDB (vector store) + OpenAI Embeddings
- **Framework**: Streamlit
- **Language**: Python 3.11

## 📦 Installation

### Prerequisites
- Python 3.11+
- OpenAI API key
- Tavily API key

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd autonomous-research-assistant
```

2. **Create conda environment**
```bash
conda create -n autonomous-research-assistant python=3.11 -y
conda activate autonomous-research-assistant
```

3. **Install dependencies**
```bash
pip install -r requirements.txt --break-system-packages
```

4. **Configure API keys**

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🚀 Usage

1. Enter your research topic in the text input
2. Click "Start Research" button
3. Watch the AI autonomously research the topic
4. View the comprehensive report with citations
5. Ask follow-up questions for deeper insights

## 📁 Project Structure
```
autonomous-research-assistant/
├── src/
│   ├── agents/          # AI agents (planner, executor, synthesizer)
│   ├── graph/           # LangGraph workflow
│   ├── llm/             # LLM client and prompts
│   ├── rag/             # RAG system (embeddings, vector store, retriever)
│   ├── tools/           # Tools (search, scraper, parser)
│   └── utils/           # Utilities (config, logging)
├── tests/               # Test files
├── data/                # Data storage (ChromaDB)
├── app.py               # Streamlit application
├── .env                 # API keys (not in repo)
├── requirements.txt     # Python dependencies
└── README.md
```

## 👤 Author

Built by **Jibin Kunjumon**

---

*🚀 Autonomous Research • 🧠 AI-Powered • 📚 RAG-Enhanced*