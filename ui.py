# ui.py (Streamlit frontend)

import streamlit as st
import requests
import uuid
import time

API_URL = "http://localhost:8000"

# --------------------------
# Utility
# --------------------------
def new_thread():
    return str(uuid.uuid4())


# --------------------------
# Session Initialization
# --------------------------
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = new_thread()

if "history" not in st.session_state:
    st.session_state["history"] = []

if "uploaded_name" not in st.session_state:
    st.session_state["uploaded_name"] = None

if "uploaded_bytes" not in st.session_state:
    st.session_state["uploaded_bytes"] = None

if "pdf_indexed" not in st.session_state:
    st.session_state["pdf_indexed"] = False


# --------------------------
# Layout
# --------------------------
st.title("History book AI Chatbot 📚  🤖")

# ------------- PDF Sidebar Upload Handling -------------
st.sidebar.header("PDF")
uploaded = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

# 1) Capture file ONLY FIRST TIME
if uploaded and not st.session_state["uploaded_name"]:
    st.session_state["uploaded_name"] = uploaded.name
    st.session_state["uploaded_bytes"] = uploaded.getvalue()
    st.session_state["pdf_indexed"] = False  # trigger ingestion


# 2) Index PDF once
if st.session_state["uploaded_bytes"] and not st.session_state["pdf_indexed"]:
    with st.sidebar:
        with st.spinner("Indexing PDF… This may take a moment."):
            files = {
                "pdf": (
                    st.session_state["uploaded_name"],
                    st.session_state["uploaded_bytes"],
                    "application/pdf",
                )
            }
            data = {"thread_id": st.session_state["thread_id"]}

            res = requests.post(f"{API_URL}/ingest", data=data, files=files)
            st.session_state["pdf_indexed"] = True

        st.success("PDF indexed!")


# 3) Show status
if st.session_state["pdf_indexed"]:
    st.sidebar.success(f"Using PDF: {st.session_state['uploaded_name']}")


# ------------- New Chat -------------
def reset_chat():
    st.session_state["thread_id"] = new_thread()
    st.session_state["history"] = []
    st.session_state["uploaded_name"] = None
    st.session_state["uploaded_bytes"] = None
    st.session_state["pdf_indexed"] = False


st.sidebar.button("New Chat", on_click=reset_chat)


# --------------------------
# Chat Display
# --------------------------
for msg in st.session_state["history"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# --------------------------
# Chat Input
# --------------------------
user_msg = st.chat_input("Ask something about your PDF...")

if user_msg:
    # Add user message
    st.session_state["history"].append({"role": "user", "content": user_msg})

    # Call backend
    payload = {
        "message": user_msg,
        "thread_id": st.session_state["thread_id"],
    }

    resp = requests.post(f"{API_URL}/chat", json=payload).json()
    ai_msg = resp["response"]

    # Add assistant message
    st.session_state["history"].append({"role": "assistant", "content": ai_msg})

    st.rerun()
