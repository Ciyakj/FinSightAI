# utils/web_scraper.py

import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_moneycontrol_financials(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Look for financial tables inside divs with class 'mctable1' (Moneycontrol pattern)
        tables = soup.find_all("table", {"class": "mctable1"})

        if not tables:
            return "No readable tables found."

        dfs = []
        for table in tables:
            df = pd.read_html(str(table), flavor="bs4")[0]
            if not df.empty:
                dfs.append(df)

        return dfs if dfs else "No financial data extracted."

    except Exception as e:
        return f"Web scrape error: {str(e)}"
