from llm_response import get_llm_response

def get_answer_to_query(query):
    prompt = f"You are a helpful medical assistant! You only respond to medical queries and say 'I don't know'' for anything else!"
    response = get_llm_response(prompt, query)
    return response
