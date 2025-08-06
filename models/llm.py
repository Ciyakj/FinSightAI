# models/llm.py
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from config.config import GROQ_API_KEY, DEFAULT_MODEL

def ask_llm(prompt):
    try:
        chat = ChatGroq(api_key=GROQ_API_KEY, model=DEFAULT_MODEL)
        messages = [
            SystemMessage(content="You are a helpful financial analyst AI that explains and interprets balance sheets, profit/loss statements, and key company financials."),
            HumanMessage(content=prompt)
        ]
        response = chat.invoke(messages)
        return response.content
    except Exception as e:
        return f"Groq API Error: {str(e)}"
