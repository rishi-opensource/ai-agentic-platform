import sys
from pathlib import Path

# Path helper
sys.path.append(str(Path(__file__).parent.parent))

from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from src.llm.groq_client import get_groq_client
from langgraph.prebuilt import create_react_agent

# --- TOOL DEFINITIONS ---

# 1. Custom Calculator Tool
@tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together. Use this for ANY math calculation."""
    return a * b

# 2. Search Tool
search_tool = TavilySearch(k=2)

# List of tools available to our agent
tools = [search_tool, multiply]

# --- MAIN EXECUTION ---

def main():
    # 1. Setup the LLM
    llm = get_groq_client()
    
    # 2. Create the Agent with BOTH tools
    agent_executor = create_react_agent(llm, tools)
    
    # 3. Ask a COMPLEX multi-part question
    query = "What is 123.45 * 678.9 and who is the current CEO of Apple?"
    print(f"\n--- Starting Multi-Tool Agent ---")
    print(f"Query: {query}")
    
    inputs = {"messages": [("user", query)]}
    
    # Run the loop
    for chunk in agent_executor.stream(inputs, stream_mode="values"):
        message = chunk["messages"][-1]
        
        # This part is fun: It shows which tool the AI picked!
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tc in message.tool_calls:
                print(f"👉 AI chose tool: {tc['name']} with args: {tc['args']}")

    print("\n--- Final Answer from AI ---")
    print(message.content)

if __name__ == "__main__":
    main()
