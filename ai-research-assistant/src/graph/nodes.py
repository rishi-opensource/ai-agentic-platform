from src.graph.state import AgentState
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from src.llm.groq_client import get_groq_client

# --- TOOL DEFINITIONS ---

@tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together. Use this for ANY math calculation."""
    return a * b

# 2. Setup the Tools
search_tool = TavilySearch(k=2)
tools = [search_tool, multiply]

# 3. Setup the LLM and bind the tools
llm = get_groq_client()
llm_with_tools = llm.bind_tools(tools)

def research_node(state: AgentState):
    """
    The Researcher: Decide if we need to search or if we have enough info.
    """
    messages = state["messages"]
    
    # We add a small system instruction to keep the researcher focused
    system_instruction = SystemMessage(content="You are a research assistant. If you need more information, use the search tool. If you have enough info, just say 'I have enough information to summarize.'")
    
    # Call the LLM with the current message history
    response = llm_with_tools.invoke([system_instruction] + messages)
    
    # Return an update to the state (appending the new message)
    return {"messages": [response]}

def summarize_node(state: AgentState):
    """
    The Summarizer: Take everything we found and write a clean report.
    """
    messages = state["messages"]
    
    # A prompt specifically for the final summary
    summarize_prompt = SystemMessage(content="Write a concise 3-paragraph research report based on the findings in the conversation. Use a professional tone.")
    
    response = llm.invoke([summarize_prompt] + messages)
    
    return {"messages": [response], "is_complete": True}
