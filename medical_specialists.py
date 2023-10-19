from llm_response import get_llm_response

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
