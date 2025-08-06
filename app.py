import streamlit as st
import pandas as pd
from models.llm import call_llm
from utils.web_search import live_search
from utils.web_scraper import fetch_moneycontrol_financials

# 🔧 App configuration
st.set_page_config(page_title="FinSight AI")
st.title("📊 FinSight AI – Analyze Financial Reports Instantly")

# 🔘 User options
mode = st.selectbox("🔧 Choose response mode", ["concise", "detailed"])
model = st.selectbox("🤖 Choose LLM model", ["groq", "gemini", "deepseek"])

# 🔗 User input
url_input = st.text_input("📊 Enter Moneycontrol Financials URL")
question = st.text_input("💬 Ask something about the financials:")

# 🧠 Logic for processing financial data
if url_input and question:
    st.info("🔍 Scraping financial data from Moneycontrol...")
    dfs = fetch_moneycontrol_financials(url_input)

    if isinstance(dfs, list):
        context = "\n\n".join([df.to_string(index=False) for df in dfs])
        prompt = f"You are a financial analyst. Given this financial data from {url_input}:\n\n{context}\n\nAnswer the user's question:\n{question}"
        response = call_llm(prompt)
        st.markdown(f"### 🧠 Response:\n{response}")
    else:
        st.warning(f"❌ Error: {dfs}")

else:
    st.info("📥 Please enter a Moneycontrol financial URL and your question to get started.")
