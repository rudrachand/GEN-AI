# app.py

import streamlit as st
import os
from dotenv import load_dotenv

from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from get_embedding_function import get_embedding_function

# === Load API key from .env ===
load_dotenv()
if "GOOGLE_API_KEY" not in os.environ:
    st.error("❌ Missing GOOGLE_API_KEY in .env file.")
    st.stop()

# === Constants ===
CHROMA_PATH = "chroma-history-database"
PROMPT_TEMPLATE = """
You are a knowledgeable and helpful history tutor for an 8th-grade student.
Answer the student's question using only the information provided in the sources below. Do not use outside knowledge or make assumptions.
If the answer is not present in the sources, say "I don't know based on the provided materials."
Explain your answer clearly and simply, using bullet points or short paragraphs if helpful.

Sources:
{context}

---

Question: {question}
"""

# === Initialize Gemini model ===
llm = ChatGoogleGenerativeAI(
    #model="gemini-2.5-flash",
    model = "gemini-2.5-flash-lite-preview-06-17",
    temperature=0.2,
    max_tokens=1024,
    timeout=60,
    max_retries=2
)

# === Initialize Chroma Vector DB ===
embedding_function = get_embedding_function()
vector_db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_function
)

# === Streamlit UI ===
st.set_page_config(page_title="📚 8th Class Chatbot for History", layout="wide")
st.title("🎓 8th Class Chatbot for History")
st.markdown("Ask your history questions based on 8th-grade CBSE textbooks and notes.")
st.info("📘 This chatbot is trained on 8th class history materials. Type your question below!")

# === Example Questions (optional) ===
st.markdown("💡 **Try asking one of these questions:**")
example_questions = [
    "What were the causes of the Revolt of 1857?",
    "Who were the Mughals and what was their contribution?",
    "How did British rule affect Indian agriculture?",
]

# Variable to hold chosen example (if clicked)
chosen_example = None
for q in example_questions:
    if st.button(q):
        chosen_example = q

# === User Input ===
user_query = st.text_input(
    "🔍 Enter your history question:",
    value=chosen_example if chosen_example else "",
    placeholder="E.g. What were the problems with James Mill’s periodisation of Indian history?"
)

# === RAG Inference ===
if user_query:
    with st.spinner("🔍 Searching your textbook content..."):
        results = vector_db.similarity_search_with_score(user_query, k=7)

    # Combine relevant chunks
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    # Format prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=user_query)

    with st.spinner("💡 Generating answer please wait..."):
        response = llm.invoke(prompt)

    # === Display Answer ===
    st.subheader("💬 Answer")
    st.markdown(response.content)

    # === Display Sources ===
    st.subheader("📚 Sources")
    for doc, _ in results:
        st.markdown(f"- `{doc.metadata.get('id', 'Unknown')}`")
