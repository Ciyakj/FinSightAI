import streamlit as st
import pandas as pd
from models.llm import call_llm
from models.embeddings import get_embedding
from utils.file_reader import read_code_files
from utils.rag_retriever import CodeRAGRetriever
from utils.web_search import live_search
from utils.web_scraper import fetch_moneycontrol_financials

st.set_page_config(page_title="CodeExplain AI")
st.title("🧠 CodeExplain AI – Understand Legacy Code")

mode = st.selectbox("🔧 Choose response mode", ["concise", "detailed"])
model = st.selectbox("🤖 Choose LLM model", ["groq", "gemini", "deepseek"])

uploaded_files = st.file_uploader("📁 Upload code files", type=["py", "js", "java", "txt", "md"], accept_multiple_files=True)
url_input = st.text_input("📊 Enter Moneycontrol Financials URL")
question = st.text_input("💬 Ask something about the code or financials:")

if uploaded_files and question:
    st.info("📦 Processing uploaded files...")
    content = read_code_files(uploaded_files)
    chunks = content.split("\n\n")
    retriever = CodeRAGRetriever()
    retriever.add_chunks(chunks)
    context = "\n\n".join(retriever.query(question))

    prompt = f"Here is some code context:\n{context}\n\nUser question: {question}"
    response = call_llm(prompt)

    if "[Error" in response or "LLM Error" in response:
        st.warning("⚠️ LLM failed. Using web search instead.")
        response = live_search(question)

    st.markdown(f"### 🧠 Response:\n{response}")

elif url_input and question:
    st.info("🔍 Scraping financial data from Moneycontrol...")
    dfs = fetch_moneycontrol_financials(url_input)
    if isinstance(dfs, list):
        context = "\n\n".join([df.to_string(index=False) for df in dfs])
        prompt = f"Here is financial data scraped from {url_input}:\n\n{context}\n\nUser question: {question}"
        response = call_llm(prompt)
        st.markdown(f"### 🧠 Response:\n{response}")
    else:
        st.warning(f"❌ Error: {dfs}")

else:
    st.info("⬆️ Upload files or enter a financial URL and ask a question to get started.")
