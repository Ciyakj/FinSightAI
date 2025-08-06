import streamlit as st
import pandas as pd
from models.llm import call_llm
from utils.web_scraper import fetch_moneycontrol_financials
from utils.rag_retriever import FinanceRAGRetriever  # Updated name

st.set_page_config(page_title="FinSight AI")
st.title("📊 FinSight AI – Analyze Financial Reports Instantly")

mode = st.selectbox("🔧 Choose response mode", ["concise", "detailed"])
model = st.selectbox("🤖 Choose LLM model", ["groq", "gemini", "deepseek"])

url_input = st.text_input("📊 Enter Moneycontrol Financials URL")
question = st.text_input("💬 Ask something about the financials:")

if url_input and question:
    st.info("🔍 Scraping financial data from Moneycontrol...")
    dfs = fetch_moneycontrol_financials(url_input)

    if isinstance(dfs, list):
        context_chunks = []
        for df in dfs:
            if isinstance(df, pd.DataFrame):
                context_chunks.append(df.to_string(index=False))

        context_text = "\n\n".join(context_chunks)

        # 🔄 RAG: Retrieve relevant chunks using embedding-based retrieval
        rag = FinanceRAGRetriever()  # Use the renamed retriever
        rag.add_chunks(context_text.split("\n\n"))
        relevant_context = "\n\n".join(rag.query(question))

        # 📌 Construct a clean prompt for the LLM
        prompt = f"""You are a financial analyst AI. Use the financial data below to answer the user's question.

## Financial Data
{relevant_context}

## User Question
{question}
"""

        response = call_llm(prompt)

        st.subheader("🧠 Response")
        st.write(response)

    else:
        st.warning(f"❌ Error: {dfs}")
else:
    st.info("📥 Please enter a Moneycontrol financial URL and your question to get started.")
