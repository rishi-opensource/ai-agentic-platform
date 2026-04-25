import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from langchain_core.messages import HumanMessage
from orchestrator import graph

console = Console()

def run_cli():
    console.print(Panel.bold("🚀 AWS Multi-Agent Infrastructure Assistant (Phase 4)", style="blue"))
    console.print("Type 'exit' or 'quit' to stop.\n")

    # Initial config with thread_id for memory
    config = {"configurable": {"thread_id": "1"}}

    while True:
        try:
            user_input = console.input("[bold green]You:[/bold green] ")
            
            if user_input.lower() in ["exit", "quit"]:
                break
            
            # Run graph with config
            input_state = {"messages": [HumanMessage(content=user_input)]}
            final_state = graph.invoke(input_state, config=config)
            
            # Display Trace (Thinking)
            if final_state.get("steps"):
                console.print("\n[bold yellow]🔍 Execution Trace:[/bold yellow]")
                for step in final_state["steps"]:
                    console.print(f"  → {step}")
            
            # Display last AI response
            last_msg = final_state["messages"][-1]
            console.print("\n[bold blue]Assistant:[/bold blue]")
            console.print(Markdown(last_msg.content))
            console.print("-" * 20)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    run_cli()
