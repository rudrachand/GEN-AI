import streamlit as st
import openai
import pprint
from dotenv import load_dotenv
import os

load_dotenv("config.env")  # Load environment variables from config.env file

openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
    st.title("Financial Assistant")
    st.markdown("This application provides financial guidance.")

    messages = get_messages()
    for message in messages:
        if message["role"] == "user":
            st.text_input("You:", value=message["content"], key=message["content"], disabled=True)
        else:
            st.text_area("Assistant:", value=message["content"], height=100, max_chars=None, key=message["content"], disabled=True)

    user_input = st.text_input("Ask me finance stuff:", "", key="user_input")
    if user_input:
        with st.spinner("Waiting for the assistant's response..."):
            messages = update_chat(messages, role="user", content=user_input)
            model_response = get_chat(messages)
            messages = update_chat(messages, role="assistant", content=model_response)
            st.text_area("Finance Bot:", value=model_response, height=100, max_chars=None, key=model_response, disabled=True)
    else:
        if st.button("Send", key="no_input_send"):
            st.text("Thanks and have a nice day ahead!")


def get_messages():
    return [
        {"role": "system", "content": "You are a financial guide in the Indian financial sector. Answer only if you are confident enough; otherwise, say 'I don't have any idea'."},
        {"role": "user", "content": "Hey, I am Rudra. I want to ask for a few financial help from you!"},
        {"role": "assistant", "content": "Hi Rudra, sure! I am happy to help you. Let me know how I can assist you with financial aspects."},
    ]


def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


def get_chat(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response['choices'][0]['message']['content']


if __name__ == "__main__":
    main()
