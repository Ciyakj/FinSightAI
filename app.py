import streamlit as st
import pandas as pd
from models.llm import call_llm
from utils.web_scraper import fetch_moneycontrol_financials
from utils.rag_retriever import CodeRAGRetriever

st.set_page_config(page_title="FinSight AI")
st.title("\U0001F4CA FinSight AI – Analyze Financial Reports Instantly")

mode = st.selectbox("\U0001F527 Choose response mode", ["concise", "detailed"])
model = st.selectbox("\U0001F916 Choose LLM model", ["groq", "gemini", "deepseek"])

url_input = st.text_input("\U0001F4CA Enter Moneycontrol Financials URL")
question = st.text_input("\U0001F4AC Ask something about the financials:")

if url_input and question:
    st.info("\U0001F50D Scraping financial data from Moneycontrol...")
    dfs = fetch_moneycontrol_financials(url_input)

    if isinstance(dfs, list):
        context_chunks = []
        for df in dfs:
            if isinstance(df, pd.DataFrame):
                context_chunks.append(df.to_string(index=False))

        context_text = "\n\n".join(context_chunks)

        # 🔄 Use RAG for retrieval
        rag = CodeRAGRetriever()
        rag.add_chunks(context_text.split("\n\n"))
        relevant_context = "\n\n".join(rag.query(question))

        prompt = f"Here is financial data context:\n{relevant_context}\n\nUser question: {question}"
        response = call_llm(prompt)

        st.markdown(f"### \U0001F4DA Response:\n{response}")
    else:
        st.warning(f"❌ Error: {dfs}")
else:
    st.info("📥 Please enter a Moneycontrol financial URL and your question to get started.")
