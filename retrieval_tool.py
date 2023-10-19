import pandas as pd
from langchain.agents import create_pandas_dataframe_agent
from langchain import OpenAI
from langchain.tools.base import StructuredTool

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
