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
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "default_user_1"

# --- CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check if we have a pending interrupt
config = {"configurable": {"thread_id": st.session_state.thread_id}}
state_snapshot = research_graph.get_state(config)

# 1. Handle Pending Approval
if state_snapshot.next:
    st.warning("🚦 **Breakpoint Reached**: Research is complete, but needs your approval to generate the final report.")
    
    # HITL Buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button("✅ Approve", use_container_width=True):
            with st.chat_message("assistant"):
                with st.status("✍️ Synthesizing Final Report...", expanded=True):
                    for chunk in research_graph.stream(None, config=config, stream_mode="updates"):
                        pass
                    final_state = research_graph.get_state(config)
                    final_report = final_state.values["messages"][-1].content
                    st.session_state.messages.append({"role": "assistant", "content": final_report})
                    st.markdown(final_report)
                    st.rerun()

    with col2:
        if st.button("❌ Reject", use_container_width=True):
            st.session_state.show_feedback = True

    # Feedback Loop UI
    if st.session_state.get("show_feedback"):
        feedback = st.text_input("💡 What should the agent improve?", placeholder="e.g. Focus more on the security protocol...")
        if st.button("📤 Send Feedback & Refine"):
            # 🔄 THE BACKTRACK TRICK
            feedback_msg = HumanMessage(content=f"Human Feedback: {feedback}")
            research_graph.update_state(config, {"messages": [feedback_msg]}, as_node="tools")
            
            st.session_state.show_feedback = False
            # Trigger a rerun so the 'else' block (the execution loop) starts again
            st.rerun()
            
    with col3:
        st.info("Approve to finish, or Reject to provide feedback and refine the research.")

# 2. Input for new message (Only if not waiting for approval)
else:
    if prompt := st.chat_input("What would you like me to research?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            output_container = st.empty()
            
            with st.status("🧠 Agent Orchestration...", expanded=True) as status:
                run_config = {
                    "configurable": {"thread_id": st.session_state.thread_id},
                    "metadata": {"model": model_choice, "interface": "streamlit"},
                }

                for chunk in research_graph.stream(
                    {"messages": [HumanMessage(content=prompt)]}, 
                    config=run_config,
                    stream_mode="updates"
                ):
                    for node_name, output in chunk.items():
                        status.write(f"✅ Executing Node: **{node_name}**")
            
            # Check if we hit an interrupt inside the loop
            final_snapshot = research_graph.get_state(run_config)
            if final_snapshot.next:
                st.warning("📊 Research loop finished. **Waiting for Approval...**")
                st.rerun() # Trigger a rerun to show the Approval UI we defined above
            else:
                final_response = final_snapshot.values["messages"][-1].content
                output_container.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
