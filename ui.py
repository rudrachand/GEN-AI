# ui.py (Streamlit frontend)

import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

# --------------------------
# Utility
# --------------------------
def new_thread():
    return str(uuid.uuid4())


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = new_thread()

if "history" not in st.session_state:
    st.session_state["history"] = []


# --------------------------
# Layout
# --------------------------
st.title("LangGraph RAG Chatbot (FastAPI + Streamlit)")

st.sidebar.header("PDF")
uploaded = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

if uploaded:
    with st.sidebar:
        st.info("Uploading...")
        files = {"pdf": (uploaded.name, uploaded.getvalue(), "application/pdf")}
        data = {"thread_id": st.session_state["thread_id"]}
        r = requests.post(f"{API_URL}/ingest", data=data, files=files)
        st.success("PDF indexed!")

st.sidebar.button("New Chat", on_click=lambda: (
    st.session_state.update({"thread_id": new_thread(), "history": []})
))


# --------------------------
# Chat Display
# --------------------------
for m in st.session_state["history"]:
    with st.chat_message(m["role"]):
        st.write(m["content"])

user_msg = st.chat_input("Ask something...")

if user_msg:
    st.session_state["history"].append({"role": "user", "content": user_msg})

    payload = {"message": user_msg, "thread_id": st.session_state["thread_id"]}
    resp = requests.post(f"{API_URL}/chat", json=payload).json()

    ai_msg = resp["response"]
    st.session_state["history"].append({"role": "assistant", "content": ai_msg})

    st.rerun()
