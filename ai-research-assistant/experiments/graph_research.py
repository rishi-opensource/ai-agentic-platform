import sys
from pathlib import Path

# Path helper
sys.path.append(str(Path(__file__).parent.parent))

from src.graph.graph import research_graph
from langchain_core.messages import HumanMessage

def main():
    # 1. Prepare the input
    # We provide a complex query that requires search and synthesis
    query = "Tell me about Project Antigravity and the reactor security protocol. Also multiply 12.5 by 8."
    print(f"--- Launching Research Graph ---")
    print(f"Query: {query}\n")
    
    inputs = {"messages": [HumanMessage(content=query)]}
    
    # 2. Config with Thread ID (Mandatory for Checkpointers)
    config = {"configurable": {"thread_id": "test_thread_123"}}
    
    # We'll keep track of the last node to print labels
    final_message = None
    
    # Stream the graph with the config
    for chunk in research_graph.stream(inputs, config=config, stream_mode="updates"):
        for node_name, output in chunk.items():
            print(f"\n📍 [Node: {node_name}]")
            
            if isinstance(output, dict) and "messages" in output:
                final_message = output["messages"][-1]
                # INSPECT: What did we actually get?
                if hasattr(final_message, "tool_calls") and final_message.tool_calls:
                    print(f"  AI wants to use tools: {[tc['name'] for tc in final_message.tool_calls]}")
                elif final_message.type == "tool":
                    print(f"  Tool returned data successfully.")
                else:
                    print(f"  Content Preview: {final_message.content[:200]}...")
            else:
                print(f"  Action required or internal state change.")

    # 3. Handle Interrupts (HITL)
    snapshot = research_graph.get_state(config)
    if snapshot.next:
        print(f"\n🚦 BREAKPOINT: The graph is paused before: {snapshot.next}")
        user_approval = input("📝 Research is complete. Approve final report? (yes/no): ").strip().lower()
        
        if user_approval == "yes":
            print("🚀 Approval received! Continuing to final summary...")
            # To resume, we stream with None as input
            for chunk in research_graph.stream(None, config=config, stream_mode="updates"):
                for node_name, output in chunk.items():
                    print(f"📍 [Node: {node_name}] (Resumed)")
                    final_message = output["messages"][-1]
        else:
            print("🛑 Approval denied. Research session paused.")
            return

    print("\n--- FINAL RESEARCH REPORT ---")
    if final_message and getattr(final_message, "content", None):
        print(final_message.content)
    else:
        print(f"⚠️ Warning: Final message content was empty! Raw: {final_message}")


if __name__ == "__main__":
    main()
