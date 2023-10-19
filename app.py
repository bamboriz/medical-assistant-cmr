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
    with open('prompts/medical_query_prompt.txt', 'r') as file:
        prompt_template = file.read()
    prompt = prompt_template.format(query=query)
    response = agent.run(prompt)
    return response

st.set_page_config(page_title="👨‍💻 Chat with Medico")

st.title("👨‍💻 Chat with Medico")

query = st.text_area("Send a Message")

if st.button("Submit Query", type="primary"):
    response = get_response(query)
    st.write(response)

