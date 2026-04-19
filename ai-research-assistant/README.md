# 🔬 Modular AI Research Assistant

A high-performance, autonomous research agent built with **LangGraph**, **Groq**, and **Tavily**. This assistant performs multi-step web research, math calculations, and stateful information synthesis with a professional **Human-in-the-loop** workflow.

## 🚀 Key Features
- **Deterministic State Machine**: Powered by LangGraph to handle complex, iterative research loops.
- **Extreme Speed**: Uses Groq (`llama-3.3-70b-versatile`) for near-instant inference.
- **Autonomous Tool-Calling**: Integrated with Tavily Search for real-time web data and custom math tools.
- **Local RAG Pipeline**: Built-in context retrieval using ChromaDB for local document analysis.
- **Human-in-the-Loop (HITL)**: Mandatory approval breakpoints before final report generation.
- **Reject & Refine Loop**: Bidirectional feedback loop allowing users to steer the agent's research.

## 🏗️ Architecture
The system uses a **Node-based graph architecture**:
1. **Researcher Node**: Analyzes the query and decides whether to use tools or summarize.
2. **Tools Node**: Executes web searches or calculations.
3. **Summarizer Node**: Synthesizes all gathered information into a final markdown report.
4. **Breakpoints**: The graph pauses before summarization, awaiting human approval or feedback.

## 📚 Learning Roadmap (Step-by-Step Docs)
This project was built in phases. You can follow the development journey here:

1.  **[LLM Basics](docs/01_llm_basics.md)**: Setting up Groq and basic inference.
2.  **[Chains & Prompts](docs/02_langchain_chains.md)**: Building reusable LLM pipelines.
3.  **[RAG Deep Dive](docs/03_rag.md)**: Document ingestion and vector search.
4.  **[Tools & Agents](docs/04_tools_agents.md)**: Empowering the LLM with search and math.
5.  **[LangGraph Orchestration](docs/05_langgraph.md)**: Moving from linear chains to stateful graphs.
6.  **[Observability](docs/06_langsmith.md)**: Professional tracing with LangSmith.
7.  **[Human-in-the-Loop](docs/09_hitl.md)**: Implementing persistence and interactive breakpoints.

## 🛠️ Setup & Installation

### 1. Prerequisites
- [uv](https://github.com/astral-sh/uv) (Extremely fast Python package manager)
- [Groq API Key](https://console.groq.com/)
- [Tavily API Key](https://tavily.com/)

### 2. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd ai-research-assistant

# Install dependencies
uv sync
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
LANGSMITH_API_KEY=your_key_here
```

## 🖥️ Usage

### Run the Interactive Dashboard
```bash
uv run streamlit run app/streamlit_app.py
```

### Run Experiments (Interactive CLI)
```bash
uv run experiments/graph_research.py
```

## 📁 Project Structure
- `src/graph/`: LangGraph orchestration and node definitions.
- `src/rag/`: Vector database and retrieval logic.
- `app/`: Streamlit dashboard and UI.
- `experiments/`: Step-by-step learning scripts and verification harnesses.
- `docs/`: Technical deep-dives for each feature.

---
Built by Antigravity with LangChain, LangGraph, and Groq.
