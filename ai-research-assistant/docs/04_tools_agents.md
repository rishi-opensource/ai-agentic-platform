# Phase 4: Tools & Agents

Until now, our assistant has been "trapped" in a box. It could only use its internal training or the specific documents we gave it (RAG). 

**Tools** give the assistant "hands." An **Agent** is the brain that decides which tool to pick up.

## 1. What is a "Tool"?
In LangChain, a Tool is basically a Python function that the LLM is allowed to call. 
Examples:
- `Google Search`: For current events.
- `Calculator`: For precise math (LLMs are surprisingly bad at math!).
- `Python REPL`: To write and run code.

## 2. How "Tool Calling" Works
This is the most important part to learn. The LLM does **not** actually run the code.
1.  **AI Decides**: "I need to know the price of Bitcoin."
2.  **AI Outputs a Request**: It sends a special message: `Call Tool: TavilySearch(query="bitcoin price")`.
3.  **The System Runs it**: Your Python code sees that request, runs the search, and gets the result.
4.  **AI Answers**: The result is fed back to the AI, and it finally says "The price of Bitcoin is $XXXXX."

## 3. Agents: The "Loop"
An **Agent** is a system that runs in a loop:
1.  **Plan**: What should I do?
2.  **Action**: Call a tool.
3.  **Observation**: Look at what the tool returned.
4.  **Repeat**: Do I have the final answer yet? If not, go back to step 1.

---

### Phase 4 Goal
We will build a simple agent that can:
1. Search the web using **Tavily**.
2. Answer questions about real-time news.
