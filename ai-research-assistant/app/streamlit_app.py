import streamlit as st
import sys
from pathlib import Path

# Path helper to find our src folder
sys.path.append(str(Path(__file__).parent.parent))

from src.graph.graph import research_graph
from langchain_core.messages import HumanMessage, AIMessage

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Pro Research AI",
    page_icon="🔬",
    layout="wide"
)

# --- SIDEBAR & SETTINGS ---
with st.sidebar:
    st.header("⚙️ Agent Settings")
    model_choice = st.selectbox("LLM Engine", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    st.divider()
    st.info("The Agent is currently in **Autonomous Mode**. It will decide which tools to use based on your query.")
    
    if st.button("Reset Session"):
        st.session_state.messages = []
        st.rerun()

st.title("🔬 Pro AI Research Assistant")
st.markdown("---")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CHAT INTERFACE ---

# Display chat history with nice styling
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new message
if prompt := st.chat_input("What would you like me to research?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Run the Graph
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # We stream the results to show progress
        final_response = ""
        nodes_visited = []
        
        # Using status for the internal thinking steps
        with st.status("🧠 Agent Orchestration...", expanded=True) as status:
            # LangSmith Configuration & Metadata
            config = {
                "metadata": {
                    "model": model_choice,
                    "interface": "streamlit",
                    "thread_id": "st_session"
                },
                "tags": ["research_assistant", "v1_demo"]
            }

            for chunk in research_graph.stream(
                {"messages": [HumanMessage(content=prompt)]}, 
                config=config,
                stream_mode="updates"
            ):
                for node_name, output in chunk.items():
                    nodes_visited.append(node_name)
                    status.write(f"✅ Executing Node: **{node_name}**")
                    
                    last_msg = output["messages"][-1]
                    
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        status.write(f"🛠️ Tool Requested: {[tc['name'] for tc in last_msg.tool_calls]}")
                    elif last_msg.type == "tool":
                        status.write("📊 Data retrieved.")
                    else:
                        final_response = last_msg.content
            
            status.update(label=f"Analysis Complete ({len(nodes_visited)} steps)", state="complete", expanded=False)
        
        # Display the final summary
        message_placeholder.markdown(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        
        # Show debug info in an expander
        with st.expander("🔍 View Technical Trace"):
            st.write(f"**Flow Path:** {' ➡️ '.join(nodes_visited)}")
            st.json(st.session_state.messages[-1])
