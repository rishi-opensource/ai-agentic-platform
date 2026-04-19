# 👤🤝🤖 Human-in-the-Loop (HITL)

Human-in-the-loop is a critical design pattern for autonomous agents. It ensures that an AI doesn't run away with a hallucinated conclusion or perform a sensitive action (like generating a final report) without human oversight.

## 🚀 Key Concepts in LangGraph
1.  **Persistence (Checkpointers)**: To "pause" a graph, the system must save its State to a database (or memory). This allows the graph to be resumed minutes or hours later.
2.  **Breakpoints**: Specific points in the graph where execution *always* stops.
3.  **Interrupts**: Dynamic pauses that happen based on the AI's logic (e.g., "I'm not sure about this search result, please verify").

## 🛠️ Implementation
We are using `MemorySaver` as our checkpointer and setting a breakpoint at the `summarizer` node.

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = workflow.compile(
    checkpointer=memory,
    interrupt_before=["summarizer"]
)
```

## 🖥️ UI Workflow
1.  The user asks a question.
2.  The researcher performs its loops.
3.  The graph hits the `summarizer` node and **PAUSES**.
4.  The Streamlit UI displays a "Review & Approve" button.
5.  When the user clicks "Approve", the graph resumes and writes the final report.
