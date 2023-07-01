import streamlit as st
from streamlit_chat import message
import openai
from dotenv import load_dotenv
import os
load_dotenv("config.env")  # Load environment variables from config.env file

from utils import *

openai.api_key = os.getenv('OPENAI_API_KEY')

st.title("Medibot : Medical Consultation~ChatGPT and Streamlit Chat")
st.subheader("Medi Consultant:")

model = st.selectbox(
    "Select a model",
    ("gpt-3.5-turbo","NA")
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Query: ", key="input")

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    with st.expander("Show Messages"):
        st.write(messages)




