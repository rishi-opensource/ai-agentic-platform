from typing import TypedDict, List, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """
    The state of the multi-agent system.
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str  # The next node to execute
    plan: List[str]  # The high-level plan (optional, for the supervisor)
    steps: Annotated[List[str], operator.add]  # Execution trace
    tool_results: Annotated[List[Dict], operator.add] # Results from tools
