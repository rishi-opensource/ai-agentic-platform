import sys
from pathlib import Path
# Tell Python to look in the root folder for our code
sys.path.append(str(Path(__file__).parent.parent))

from langchain_tavily import TavilySearch
from src.llm.groq_client import get_groq_client
from langchain_core.messages import HumanMessage

def main():
    # 1. Initialize our Search Tool
    # k=2: Just get the top 2 results to keep it simple
    search_tool = TavilySearch(k=2)
    
    # 2. Get the Groq Client
    llm = get_groq_client()
    
    # 3. "Bind" the tool to the LLM
    # This tells the LLM: "Hey, you are now allowed to use this specific search tool."
    llm_with_tools = llm.bind_tools([search_tool])
    
    # 4. Ask a question that REQUIRES the web
    query = "What is the current stock price of NVIDIA?"
    print(f"--- Asking AI: {query} ---")
    
    # 5. Invoke the LLM
    response = llm_with_tools.invoke([HumanMessage(content=query)])
    
    # 6. LOOK COSELY AT THE OUTPUT!
    print("\n--- Raw AI Response ---")
    print(response)
    
    print("\n--- Inspecting Tool Calls ---")
    if response.tool_calls:
        for tool_call in response.tool_calls:
            print(f"AI wants to call: {tool_call['name']}")
            print(f"With these arguments: {tool_call['args']}")
    else:
        print("The AI didn't feel it needed a tool for this.")

if __name__ == "__main__":
    main()
