import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from config import *
from retrieval_tool import info_retrieval_tool

st.set_page_config(page_title="👨‍💻 Chat with Medico")

st.title("👨‍💻 Chat with Medico")

query = st.text_area("Send a Message")

from response_handler import get_response

if st.button("Submit Query", type="primary"):
    response = get_response(query)
    st.write(response)

