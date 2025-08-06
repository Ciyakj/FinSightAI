# utils/web_scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_moneycontrol_financials(company_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(company_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # Locate financial tables (this works for Moneycontrol as of 2025)
        tables = soup.find_all("table", class_="mctable1")

        dataframes = []
        for table in tables:
            rows = table.find_all("tr")
            headers = [th.text.strip() for th in rows[0].find_all("th")]
            df_rows = []
            for row in rows[1:]:
                cols = [td.text.strip().replace("\n", "") for td in row.find_all("td")]
                df_rows.append(cols)
            df = pd.DataFrame(df_rows, columns=headers)
            dataframes.append(df)

        return dataframes if dataframes else "No financial data tables found."

    except Exception as e:
        return f"Web scrape error: {str(e)}"

# Example usage:
# url = "https://www.moneycontrol.com/financials/tcs/consolidated-profit-lossVI/TCH"
# dfs = fetch_moneycontrol_financials(url)
# print(dfs[0].head()) if isinstance(dfs, list) else print(dfs)

