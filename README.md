# Autonomous Research Assistant

> A multi-agent LangGraph system that takes a research question, autonomously plans subtopics, searches and scrapes the web, indexes documents into a vector store, and synthesizes a structured research brief — all without human-in-the-loop.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-multi--agent-green)](https://github.com/langchain-ai/langgraph)
[![OpenAI](https://img.shields.io/badge/GPT--4o--mini-OpenAI-412991?logo=openai)](https://openai.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-vector--store-orange)](https://www.trychroma.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Tavily](https://img.shields.io/badge/Tavily-web--search-blue)](https://tavily.com)

---

## What This Is

Most "research AI" demos hit a search API and summarize the top result. This goes further: it decomposes the research question into subtopics, runs parallel document collection, embeds everything into ChromaDB, and uses a RAG-based Synthesizer agent to write a coherent report grounded in actual retrieved evidence.

The interesting part is the agent coordination layer — three specialized agents (Planner, Executor, Synthesizer) each own a distinct phase, and LangGraph manages the state machine between them. There's no hardcoded prompt chain; the graph is declarative.

---

## Demo

[![Demo Video](https://img.youtube.com/vi/RTPbNBaLJC0/maxresdefault.jpg)](https://youtu.be/RTPbNBaLJC0)

> 📹 [Watch the full demo on YouTube](https://youtu.be/RTPbNBaLJC0)

---

## Architecture

The system is organized into 7 layers:

```
Layer 6 — Streamlit UI
    ↕
Layer 5 — LangGraph Workflow (state graph, node routing, orchestration)
    ↕
Layer 4 — Agents
    ├── Planner Agent   → decomposes query into N subtopics
    ├── Executor Agent  → fetches and parses documents per subtopic
    └── Synthesizer Agent → RAG synthesis over collected docs
    ↕
Layer 3 — RAG Stack
    ├── Embeddings: OpenAI text-embedding-3-small
    ├── Vector Store: ChromaDB (persistent)
    └── Retriever: semantic search, top-k
    ↕
Layer 2 — Tools
    ├── Web Search: Tavily API
    ├── Scraper: BeautifulSoup
    └── Document Parser: PDF + HTML → clean text
    ↕
Layer 1 — LLM
    ├── OpenAI GPT-4o-mini (chat completions)
    └── Prompt templates per agent role
    ↕
Layer 0 — Config + Logging
    └── .env, logging setup, constants
```

### Workflow

```
User Input
    → Planner Agent     (generates subtopics list)
    → Executor Agent    (fetches docs for each subtopic)
    → Synthesizer Agent (retrieves from ChromaDB, generates report)
    → Final Report + Interactive Q&A
```

The LangGraph state graph tracks which subtopics have been researched, what documents have been indexed, and which agent runs next. Each agent node reads from and writes to a shared `ResearchState` TypedDict.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent orchestration | LangGraph |
| LLM | GPT-4o-mini (OpenAI) |
| Embeddings | text-embedding-3-small (OpenAI) |
| Vector store | ChromaDB |
| Web search | Tavily API |
| Web scraping | BeautifulSoup4 |
| API layer | FastAPI |
| UI | Streamlit |
| Language | Python 3.11 |

---

## Setup

### Prerequisites

- Python 3.11+
- OpenAI API key
- Tavily API key

### Installation

```bash
git clone https://github.com/jibz33on/autonomous-research-assistant
cd autonomous-research-assistant

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
CHROMA_PERSIST_DIR=./chroma_db
```

### Run

```bash
# Streamlit UI
streamlit run app.py

# Or FastAPI backend only
uvicorn main:app --reload
```

---

## Project Structure

```
autonomous-research-assistant/
├── app.py                  # Streamlit frontend
├── main.py                 # FastAPI entry point
├── config/
│   └── settings.py         # Env vars, constants
├── llm/
│   ├── client.py           # OpenAI client setup
│   └── prompts.py          # System prompts per agent
├── tools/
│   ├── search.py           # Tavily web search
│   ├── scraper.py          # BeautifulSoup scraper
│   └── parser.py           # Document parsing
├── rag/
│   ├── embeddings.py       # text-embedding-3-small
│   ├── vectorstore.py      # ChromaDB ops
│   └── retriever.py        # Semantic search
├── agents/
│   ├── planner.py          # Subtopic decomposition
│   ├── executor.py         # Document collection
│   └── synthesizer.py      # RAG-based synthesis
├── graph/
│   ├── state.py            # ResearchState TypedDict
│   ├── nodes.py            # LangGraph node definitions
│   └── workflow.py         # Graph construction + compile
└── requirements.txt
```

---

## Why It's Built This Way

**LangGraph over LangChain LCEL chains:** The research workflow has branching logic — if the Planner generates 5 subtopics, the Executor runs per subtopic, and results converge before synthesis. A linear chain can't express this cleanly. LangGraph's state graph makes the control flow explicit and debuggable.

**ChromaDB for persistence:** Each research session indexes its documents. ChromaDB persists embeddings to disk, so Q&A after the initial report doesn't require re-fetching the web — it queries the already-indexed collection.

**Separate Planner and Executor agents:** Keeping planning and execution separate makes each agent's prompt simpler and more focused. The Planner just needs to think about what to research; the Executor just needs to go get it.

---

## Author

**Jibin Kunjumon** — AI Engineer  
[GitHub](https://github.com/jibz33on) · [LinkedIn](https://linkedin.com/in/jibin-kunjumon)
