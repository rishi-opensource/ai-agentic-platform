import operator
from typing import Literal, List, TypedDict, Annotated, Sequence, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel, Field

from state import AgentState
from agents.ec2_agent import EC2_TOOLS
from agents.rds_agent import RDS_TOOLS
from agents.lambda_agent import LAMBDA_TOOLS
from prompts import SUPERVISOR_PROMPT, EC2_AGENT_PROMPT, RDS_AGENT_PROMPT, LAMBDA_AGENT_PROMPT

# Combined tools for the ToolNode
ALL_TOOLS = EC2_TOOLS + RDS_TOOLS + LAMBDA_TOOLS

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# --- Supervisor Node (The Planner) ---
class RouteResponse(BaseModel):
    next: Literal["EC2_Agent", "RDS_Agent", "Lambda_Agent", "FINISH"] = Field(
        ..., 
        description="The next agent to call or FINISH if the task is complete."
    )
    plan: List[str] = Field(..., description="The sequence of agents/tasks to carry out.")

def supervisor_node(state: AgentState):
    """
    Strategic orchestrator that plans and routes to specialized agents.
    """
    messages = state["messages"]
    
    # We use structured output for the supervisor
    supervisor_llm = llm.with_structured_output(RouteResponse)
    
    # Context message about the current plan and trace
    trace_context = f"\n\nExecution Trace: {', '.join(state.get('steps', []))}"
    if state.get('plan'):
        trace_context += f"\nOriginal Plan: {', '.join(state['plan'])}"
        
    full_messages = [SystemMessage(content=SUPERVISOR_PROMPT + trace_context)] + list(messages)
    response = supervisor_llm.invoke(full_messages)
    
    return {
        "next": response.next,
        "plan": response.plan,
        "steps": [f"Supervisor selected {response.next}"]
    }

# --- Specialized Agent Factory ---
def create_agent_node(agent_llm, tools, system_prompt, name):
    """
    Creates a specialized agent node with its own system prompt and tools.
    """
    agent_with_tools = agent_llm.bind_tools(tools)
    
    def node(state: AgentState):
        messages = state["messages"]
        # Inject system prompt
        full_messages = [SystemMessage(content=system_prompt)] + list(messages)
        result = agent_with_tools.invoke(full_messages)
        return {
            "messages": [result],
            "steps": [f"{name} invoked"]
        }
    
    return node

# Create agent nodes
ec2_node = create_agent_node(llm, EC2_TOOLS, EC2_AGENT_PROMPT, "EC2_Agent")
rds_node = create_agent_node(llm, RDS_TOOLS, RDS_AGENT_PROMPT, "RDS_Agent")
lambda_node = create_agent_node(llm, LAMBDA_TOOLS, LAMBDA_AGENT_PROMPT, "Lambda_Agent")

# --- Router Logic ---
def router(state: AgentState):
    return state["next"]

def agent_router(state: AgentState):
    """
    Determines if an agent needs tools or returned to supervisor.
    """
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "supervisor"

# Custom Tool Node to track results in state
def tool_node_with_trace(state: AgentState):
    t_node = ToolNode(ALL_TOOLS)
    result = t_node.invoke(state)
    
    # Extract tool results for the trace
    tool_msgs = [m for m in result["messages"] if isinstance(m, ToolMessage)]
    trace_steps = [f"Tool {m.name} executed" for m in tool_msgs]
    
    return {
        "messages": result["messages"],
        "steps": trace_steps
    }

# --- Build Graph ---
builder = StateGraph(AgentState)

builder.add_node("supervisor", supervisor_node)
builder.add_node("EC2_Agent", ec2_node)
builder.add_node("RDS_Agent", rds_node)
builder.add_node("Lambda_Agent", lambda_node)
builder.add_node("tools", tool_node_with_trace)

builder.set_entry_point("supervisor")

# Supervisor edges
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

# Agent loops: Agent -> Tools -> back to Agent (for reasoning)
builder.add_conditional_edges(
    "EC2_Agent",
    agent_router,
    {"tools": "tools", "supervisor": "supervisor"}
)

builder.add_conditional_edges(
    "RDS_Agent",
    agent_router,
    {"tools": "tools", "supervisor": "supervisor"}
)

builder.add_conditional_edges(
    "Lambda_Agent",
    agent_router,
    {"tools": "tools", "supervisor": "supervisor"}
)

# After tools, we need to go back to the node that CALLED them.
def tool_return_router(state: AgentState):
    return state["next"]

builder.add_conditional_edges(
    "tools",
    tool_return_router,
    {
        "EC2_Agent": "EC2_Agent",
        "RDS_Agent": "RDS_Agent",
        "Lambda_Agent": "Lambda_Agent"
    }
)

# Compile with memory
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
