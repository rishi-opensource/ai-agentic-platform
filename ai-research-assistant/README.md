# 🔬 Modular AI Research Assistant

A high-performance, autonomous research agent built with **LangGraph**, **Groq**, and **Tavily**. This assistant can perform multi-step web research, math calculations, and stateful information synthesis to produce clean, professional reports.

## 🚀 Key Features
- **Deterministic State Machine**: Powered by LangGraph to handle complex, iterative research loops.
- **Extreme Speed**: Uses Groq (`llama-3.3-70b-versatile`) for near-instant inference.
- **Autonomous Tool-Calling**: Integrated with Tavily Search for real-time web data and custom math tools.
- **Local RAG Pipeline**: Built-in context retrieval using ChromaDB for local document analysis.
- **Interactive Dashboard**: A sleek Streamlit UI with real-time "thinking" tracing.

## 🏗️ Architecture
The system uses a **Node-based graph architecture**:
1. **Researcher Node**: Analyzes the query and decides whether to use tools or summarize.
2. **Tools Node**: Executes web searches or calculations.
3. **Summarizer Node**: Synthesizes all gathered information into a final markdown report.

## 🛠️ Setup & Installation

### 1. Prerequisites
- [uv](https://github.com/astral-sh/uv) (Extremely fast Python package manager)
- [Groq API Key](https://console.groq.com/)
- [Tavily API Key](https://tavily.com/)

### 2. Installation
```bash
# Clone the repository
cd ai-research-assistant

# Install dependencies
uv sync
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

## 🖥️ Usage

### Run the Interactive Dashboard
```bash
uv run streamlit run app/streamlit_app.py
```

### Run Experiments (Console/DEBUG)
```bash
uv run experiments/graph_research.py
```

## 📁 Project Structure
- `src/graph/`: LangGraph orchestration logic.
- `src/llm/`: LLM client configurations (Groq).
- `src/rag/`: Vector database and retrieval chains.
- `app/`: Streamlit dashboard implementation.
- `experiments/`: Step-by-step learning scripts and test harnesses.

---
Built with ❤️ using LangChain, LangGraph, and Groq.
