from typing import Literal, List, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel, Field

from state import AgentState
from agents.ec2_agent import EC2_TOOLS
from agents.rds_agent import RDS_TOOLS
from agents.lambda_agent import LAMBDA_TOOLS

# Combined tools
ALL_TOOLS = EC2_TOOLS + RDS_TOOLS + LAMBDA_TOOLS

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# --- Supervisor Node ---
class RouteResponse(BaseModel):
    next: Literal["EC2_Agent", "RDS_Agent", "Lambda_Agent", "FINISH"] = Field(
        ..., 
        description="The next agent to call or FINISH if the task is complete."
    )

def supervisor_node(state: AgentState):
    """
    The central orchestrator that decides which specialized agent to invoke.
    """
    messages = state["messages"]
    
    # System prompt for the supervisor
    system_prompt = (
        "You are a supervisor managing a team of AWS specialized agents."
        " Given the user request, decide which agent should act next."
        " - EC2_Agent: Specialized in instances, VPCs, and networking."
        " - RDS_Agent: Specialized in databases and snapshots."
        " - Lambda_Agent: Specialized in serverless functions and configurations."
        " - FINISH: Select this if the user goal has been met or if you have enough information."
    )
    
    # We use structured output to ensure the supervisor returns a valid 'next' destination
    supervisor_llm = llm.with_structured_output(RouteResponse)
    
    # Prepend system prompt to the conversation for context
    response = supervisor_llm.invoke([HumanMessage(content=system_prompt)] + list(messages))
    
    return {"next": response.next}

# --- Specialized Agent Factory ---
def create_agent_node(agent_llm, tools, name):
    """
    Helper to create a node for a specialized agent.
    """
    agent_with_tools = agent_llm.bind_tools(tools)
    
    def node(state: AgentState):
        result = agent_with_tools.invoke(state["messages"])
        return {"messages": [result]}
    
    return node

# Create nodes
ec2_node = create_agent_node(llm, EC2_TOOLS, "EC2_Agent")
rds_node = create_agent_node(llm, RDS_TOOLS, "RDS_Agent")
lambda_node = create_agent_node(llm, LAMBDA_TOOLS, "Lambda_Agent")

# --- Router Logic ---
def router(state: AgentState):
    """
    Conditional logic for the supervisor.
    """
    return state["next"]

def tool_router(state: AgentState):
    """
    Determines if an agent needs to call tools or return to supervisor.
    """
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "supervisor"

# --- Build Graph ---
builder = StateGraph(AgentState)

# Add nodes
builder.add_node("supervisor", supervisor_node)
builder.add_node("EC2_Agent", ec2_node)
builder.add_node("RDS_Agent", rds_node)
builder.add_node("Lambda_Agent", lambda_node)
builder.add_node("tools", ToolNode(ALL_TOOLS))

# Define flow
builder.set_entry_point("supervisor")

# Supervisor decides where to go
builder.add_conditional_edges(
    "supervisor",
    router,
    {
        "EC2_Agent": "EC2_Agent",
        "RDS_Agent": "RDS_Agent",
        "Lambda_Agent": "Lambda_Agent",
        "FINISH": END
    }
)

# Agent loop: Agent -> Tools -> Agent or back to Supervisor
builder.add_conditional_edges(
    "EC2_Agent",
    tool_router,
    {"tools": "tools", "supervisor": "supervisor"}
)

builder.add_conditional_edges(
    "RDS_Agent",
    tool_router,
    {"tools": "tools", "supervisor": "supervisor"}
)

builder.add_conditional_edges(
    "Lambda_Agent",
    tool_router,
    {"tools": "tools", "supervisor": "supervisor"}
)

# After tools, always go back to the node that called them
# NOTE: In a more complex setup, we'd track which agent called the tool.
# For simplicity here, we can route back to supervisor or use a smarter tool router.
builder.add_edge("tools", "supervisor") # Simplest way: tools always go back to supervisor to summarize

# Compile with checkpointer for persistence
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
