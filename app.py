import streamlit as st
import openai
import os
import pandas as pd
from dotenv import load_dotenv
from langchain.agents import create_pandas_dataframe_agent
from langchain import OpenAI
from langchain.tools.base import StructuredTool
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType

load_dotenv()

OPENAI_API_KEY  = os.environ['OPENAI_API_KEY']
openai.api_key = OPENAI_API_KEY

def get_llm_response(prompt, query):
    response = openai.ChatCompletion.create(
              model="gpt-4",
              temperature = 0,
              messages=[{"role": "system", "content": prompt},
                        {"role": "user", "content": query}
              ])
    # print(response)
    return response["choices"][0]["message"]["content"]

def get_answer_to_query(query):
    prompt = f"You are a helpful medical assistant! You only respond to medical queries and say 'I don't know'' for anything else!"
    response = get_llm_response(prompt, query)
    return response

def get_medical_specialists(query):
    prompt = '''
                You are a helpful medical assistant! Your role is to detect any relevant medical specialists from the text provided.
                For general cases recommend a General Practitioner.
                Return your response as an Initial case comma-separated string when there are multiple.
                For example:
                Q: I have eye problems A: Ophthalmologist
                Q: Chest pain, pressure, tightness, or discomfort, especially if it radiates to the arms, neck, jaw, or back, can be a sign of heart problems. This can be a symptom of angina or a heart attack. A: Cardiologist
            '''
    response = get_llm_response(prompt, query)
    return response

def info_retrieval_tool():
    """
    This function will help you find the details of a medical specialist.
    :return: Medical specialist info
    """

    def get_details(specialist: str) -> str:
        data = "./data/specialist_doctors_repo.csv"
        df = pd.read_csv(data, encoding='latin-1')
        agent = create_pandas_dataframe_agent(OpenAI(temperature=0, max_tokens=512, model_name='gpt-4'), df, verbose=True)
        prompt = f''' 
            Return name, availability, location and contact info for the most relevant medical personnel.
            {specialist}
            '''
        response = agent.run(prompt)
        return response

    tool = StructuredTool.from_function(func=get_details,
                                              name='get medical specialist(s) detaills',
                                              description='This function will help you get the details of a medical specialist')

    return tool

st.set_page_config(page_title="👨‍💻 Talk with your CSV")

st.title("👨‍💻 Chat with Medico")

query = st.text_area("Send a Message")

if st.button("Submit Query", type="primary"):
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
    st.write(response)