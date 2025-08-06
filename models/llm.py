import openai
from config.config import OPENAI_API_KEY, DEFAULT_MODEL

def ask_llm(prompt):
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"LLM Error: {e}"
