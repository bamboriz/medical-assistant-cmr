import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from config import *
from retrieval_tool import info_retrieval_tool

def get_response(query):
    tools = [info_retrieval_tool()]
    llm = ChatOpenAI(temperature=0, model_name='gpt-4')
    agent = initialize_agent(llm=llm,
            tools=tools,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True)
    prompt = f'''
        You are a helpful medical assistant! You only respond to medical queries and say 'I don't know' for anything else!
        Let's decode the way to respond to the queries.
        For all medical queries in addition to providing a relevant answer, also add the details (name, availability, location and contact info ...) of 1 or more relevant Medical personnel.
        When no specialist matches, recommend a General Practitioner.
        Think step by step
        {query}
        '''
    response = agent.run(prompt)
    return response

st.set_page_config(page_title="👨‍💻 Chat with Medico")

st.title("👨‍💻 Chat with Medico")

query = st.text_area("Send a Message")

if st.button("Submit Query", type="primary"):
    response = get_response(query)
    st.write(response)

