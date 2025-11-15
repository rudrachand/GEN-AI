import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

# Disable logs (as in your script)
os.environ["MCP_USE_DEBUG_LOGGING"] = "false"
os.environ["MCP_USE_ANONYMIZED_TELEMETRY"] = "false"

load_dotenv()

# Initialize LLM
llm = ChatGroq(model="openai/gpt-oss-20b")

st.set_page_config(page_title="MCP Memory Chat", page_icon="💬", layout="wide")
st.title("🧠 MCP Memory Chat – Streamlit Web App")


# -----------------------------
# Helper: Initialize agent once
# -----------------------------
async def init_agent():
    if "agent" not in st.session_state:
        config_file = "mcp-config.json"
        client = MCPClient.from_config_file(config_file)

        agent = MCPAgent(
            llm=llm,
            client=client,
            max_steps=50,
            memory_enabled=False,
        )

        st.session_state.agent = agent
        st.session_state.client = client
        st.session_state.messages = []


# -----------------------------
# Helper: Run agent response
# -----------------------------
async def get_response(user_msg):
    agent = st.session_state.agent
    response = await agent.run(user_msg)
    return response


# -----------------------------
# Main UI
# -----------------------------
async def main():
    await init_agent()

    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Type your message...")

    if user_input:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display instantly
        with st.chat_message("user"):
            st.markdown(user_input)

        # Process response
        with st.chat_message("assistant"):
            response = await get_response(user_input)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    # Clear chat button
    if st.button("🧹 Clear Conversation"):
        st.session_state.messages = []
        st.session_state.agent.clear_conversation_history()
        st.success("Conversation history cleared!")


# Run async inside Streamlit
asyncio.run(main())
