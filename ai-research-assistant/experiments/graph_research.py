import sys
from pathlib import Path

# Path helper
sys.path.append(str(Path(__file__).parent.parent))

from src.graph.graph import research_graph
from langchain_core.messages import HumanMessage

def main():
    # 1. Prepare the input
    # We provide a complex query that requires search and synthesis
    query = "What are the top 2 latest achievements of SpaceX and what is 15% of 5000?"
    print(f"--- Launching Research Graph ---")
    print(f"Query: {query}\n")
    
    inputs = {"messages": [HumanMessage(content=query)]}
    
    # We'll keep track of the last node to print labels
    final_message = None
    for chunk in research_graph.stream(inputs, stream_mode="updates"):
        for node_name, output in chunk.items():
            print(f"\n📍 [Node: {node_name}]")
            final_message = output["messages"][-1]
            
            # INSPECT: What did we actually get?
            print(f"  Type: {type(final_message).__name__}")
            print(f"  Content length: {len(final_message.content) if hasattr(final_message, 'content') and final_message.content else 0}")
            
            if hasattr(final_message, "tool_calls") and final_message.tool_calls:
                print(f"  AI wants to use tools: {[tc['name'] for tc in final_message.tool_calls]}")
            elif final_message.type == "tool":
                print(f"  Tool returned data successfully.")
            else:
                print(f"  Content Preview: {final_message.content[:200]}...")

    print("\n--- FINAL RESEARCH REPORT ---")
    if final_message and getattr(final_message, "content", None):
        print(final_message.content)
    else:
        print(f"⚠️ Warning: Final message content was empty! Raw: {final_message}")


if __name__ == "__main__":
    main()
