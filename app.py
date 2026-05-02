import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
from langgraph.types import Command
import uuid

st.set_page_config(page_title="AI Chatbot")

# -------------------
# INIT SESSION
# -------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "pending_interrupt" not in st.session_state:
    st.session_state.pending_interrupt = None

# -------------------
# UI HEADER
# -------------------
st.title("🤖 AI Chatbot with HITL")

# -------------------
# SHOW CHAT HISTORY
# -------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------
# USER INPUT
# -------------------
user_input = st.chat_input("Ask anything...")

if user_input:
    # show immediately
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        result = chatbot.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config={"configurable": {"thread_id": st.session_state.thread_id}},
        )

        interrupts = result.get("__interrupt__", [])

        if interrupts:
            st.session_state.pending_interrupt = interrupts[0].value
        else:
            reply = result["messages"][-1].content
            st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"Error: {e}")

    st.rerun()

# -------------------
# HITL POPUP
# -------------------
if st.session_state.pending_interrupt:

    st.warning(f"⚠️ {st.session_state.pending_interrupt}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Yes"):
            result = chatbot.invoke(
                Command(resume="yes"),
                config={"configurable": {"thread_id": st.session_state.thread_id}},
            )

            reply = result["messages"][-1].content
            st.session_state.messages.append({"role": "assistant", "content": reply})

            st.session_state.pending_interrupt = None
            st.rerun()

    with col2:
        if st.button("❌ No"):
            result = chatbot.invoke(
                Command(resume="no"),
                config={"configurable": {"thread_id": st.session_state.thread_id}},
            )

            reply = result["messages"][-1].content
            st.session_state.messages.append({"role": "assistant", "content": reply})

            st.session_state.pending_interrupt = None
            st.rerun()