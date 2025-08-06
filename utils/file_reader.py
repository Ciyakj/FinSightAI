import pandas as pd

def load_financial_data(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    chunks = [f"{col}: {val}" for col, val in df.iloc[0].items()]
    return chunks
