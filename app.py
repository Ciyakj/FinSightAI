import streamlit as st
from utils.file_reader import load_financial_data
from models.llm import ask_llm
from utils.rag_retriever import FinancialRAG

st.set_page_config(page_title="FinSight AI")
st.title("💼 FinSight AI – Financial Statement Analyzer")

uploaded_file = st.file_uploader("Upload a financial statement (CSV or Excel)", type=["csv", "xlsx"])
question = st.text_input("Ask a question about the financials:")

if uploaded_file and question:
    data_chunks = load_financial_data(uploaded_file)
    retriever = FinancialRAG()
    retriever.add_chunks(data_chunks)
    context = retriever.query(question)
    full_prompt = f"Context:\n{context}\n\nQuestion: {question}"
    answer = ask_llm(full_prompt)
    st.markdown(f"### 🧠 Response:\n{answer}")
