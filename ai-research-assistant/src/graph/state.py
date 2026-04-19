from typing import Annotated, TypedDict, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    This is the "Shared Clipboard" for our Research Graph.
    """
    # The 'add_messages' reducer tells LangGraph:
    # "When a node returns a message, append it to this list."
    # This automatically tracks our Human -> AI -> Tool -> AI conversation.
    messages: Annotated[List[BaseMessage], add_messages]
    
    # We can also track non-message data
    # For example, what topic we are currently researching
    topic: str
    
    # Or a flag to signal the graph when we are satisfied with the results
    is_complete: bool
