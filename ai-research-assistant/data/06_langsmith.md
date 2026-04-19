# 🕵️‍♂️ Advanced Observability with LangSmith

LangSmith is the control center for your AI agents. While our Streamlit dashboard shows us what's happening *now*, LangSmith allows us to see what happened *always*, analyze performance, and improve our models.

## 🚀 Why LangSmith?
1. **Tracing**: See every step of the LangGraph, including hidden variables and tool outputs.
2. **Evaluation**: Score your agent's answers using other AI models (LLM-as-a-judge).
3. **Debugging**: Replay specific runs that failed to see exactly where the logic broke.
4. **Optimization**: Track token usage and latency to find bottlenecks.

## 🛠️ Setup
Add the following to your `.env` file:
```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="Research-Assistant-V1"
LANGSMITH_API_KEY="your_api_key_here"
```

## 🧠 Advanced Tracing in LangGraph
To make your trace "Searchable" in LangSmith, you can add metadata to your graph calls:

```python
config = {
    "configurable": {"thread_id": "user_123"},
    "metadata": {
        "user_tier": "premium",
        "experiment_id": "v1-baseline"
    }
}

for chunk in graph.stream(inputs, config=config):
    # Tracing happens automatically!
```

## 📊 Evaluation (The next level)
You can create a **Dataset** in LangSmith (e.g., "SpaceX Trivia") and run your agent against it to see where it succeeds or fails quantitatively.
