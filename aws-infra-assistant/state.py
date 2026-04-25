from typing import TypedDict, List, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """
    The state of the multi-agent system.
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str  # To track which agent is next (useful for multi-agent phase)
    # You can add more fields here like 'context', 'aws_profile', etc.
