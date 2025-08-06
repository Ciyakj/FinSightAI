import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_moneycontrol_financials(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # Find all tables
        tables = soup.find_all("table")

        if not tables:
            return "No tables found on the page."

        dfs = []
        for table in tables:
            try:
                df = pd.read_html(str(table))[0]
                dfs.append(df)
            except Exception:
                continue

        if not dfs:
            return "No readable tables found."

        return dfs
    except Exception as e:
        return f"Web scrape error: {str(e)}"
