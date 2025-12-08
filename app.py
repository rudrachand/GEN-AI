# app.py (FASTAPI + LangGraph backend)

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from typing import Optional

# --- import your LangGraph logic ---
from langgraph_rag import (
    chatbot,
    ingest_pdf,
    retrieve_all_threads,
    thread_document_metadata,
)

app = FastAPI()

# Allow Streamlit to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- CHAT ENDPOINT ----------
class ChatRequest(BaseModel):
    message: str
    thread_id: str


@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    messages = [HumanMessage(content=req.message)]
    config = {"configurable": {"thread_id": req.thread_id}}

    result = chatbot.invoke({"messages": messages}, config=config)
    ai_reply = result["messages"][-1].content

    return {"response": ai_reply}


# ---------- PDF INGEST ENDPOINT ----------
@app.post("/ingest")
async def ingest_endpoint(
    thread_id: str = Form(...),
    pdf: UploadFile = File(...),
):
    bytes_data = await pdf.read()
    summary = ingest_pdf(bytes_data, thread_id, pdf.filename)
    return {"summary": summary}


# ---------- THREAD LIST ----------
@app.get("/threads")
def list_threads():
    return {"threads": retrieve_all_threads()}


# ---------- THREAD DOC INFO ----------
@app.get("/thread/meta/{thread_id}")
def meta(thread_id: str):
    return thread_document_metadata(thread_id)


# To run:
# uvicorn app:app --host 0.0.0.0 --port 8000 --reload
