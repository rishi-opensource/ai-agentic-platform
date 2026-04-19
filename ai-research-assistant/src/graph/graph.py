from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from src.graph.state import AgentState
from src.graph.nodes import research_node, summarize_node, tools

# 1. Define the conditional logic
def should_continue(state: AgentState):
    """
    Decide if we should go to tools or the summarizer.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the LLM generated tool calls, we MUST go to the tools node
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # Otherwise, we are ready to summarize
    return "summarizer"

# 2. Build the Graph
workflow = StateGraph(AgentState)

# 3. Add our Nodes
workflow.add_node("researcher", research_node)
workflow.add_node("summarizer", summarize_node)
workflow.add_node("tools", ToolNode(tools)) # Prebuilt node to run tools

# 4. Define the Edges (The Flow)
workflow.add_edge(START, "researcher")

# This is a Conditional Edge: It has choices!
workflow.add_conditional_edges(
    "researcher",
    should_continue,
    {
        "tools": "tools",       # If should_continue returns 'tools' -> go to tools node
        "summarizer": "summarizer" # If returns 'summarizer' -> go to summarizer node
    }
)

# After tools run, they ALWAYS go back to the researcher to see the results
workflow.add_edge("tools", "researcher")

# After summarizer runs, we are DONE
workflow.add_edge("summarizer", END)

# 5. Compile the Graph
# This turns the blueprint into an executable "app"
research_graph = workflow.compile()
