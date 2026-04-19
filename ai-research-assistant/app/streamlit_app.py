import streamlit as st
import sys
from pathlib import Path

# Path helper to find our src folder
sys.path.append(str(Path(__file__).parent.parent))

from src.graph.graph import research_graph
from langchain_core.messages import HumanMessage, AIMessage

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 AI Research Assistant")
st.markdown("Powered by **Groq**, **Tavily**, and **LangGraph**.")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CHAT INTERFACE ---

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new message
if prompt := st.chat_input("What would you like me to research?"):
    # 1. Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Run the Graph
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        status_placeholder = st.empty()
        
        inputs = {"messages": [HumanMessage(content=prompt)]}
        
        # We stream the results to show progress
        final_response = ""
        
        # Using status for the internal thinking steps
        with st.status("Thinking...", expanded=True) as status:
            for chunk in research_graph.stream(inputs, stream_mode="updates"):
                for node_name, output in chunk.items():
                    status.write(f"📍 Active Node: **{node_name}**")
                    
                    last_msg = output["messages"][-1]
                    
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        status.write(f"🛠️ Requesting tools: {[tc['name'] for tc in last_msg.tool_calls]}")
                    elif last_msg.type == "tool":
                        status.write("✅ Tools returned data.")
                    else:
                        final_response = last_msg.content
            
            status.update(label="Research Complete!", state="complete", expanded=False)
        
        # Display the final summary
        message_placeholder.markdown(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
