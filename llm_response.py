import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_llm_response(prompt, query):
    response = openai.ChatCompletion.create(
              model="gpt-4",
              temperature = 0,
              messages=[{"role": "system", "content": prompt},
                        {"role": "user", "content": query}
              ])
    return response["choices"][0]["message"]["content"]
