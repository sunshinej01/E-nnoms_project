import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

def crawl_data(base_url, start_date):
    results = []
    page = 1

    while True:
        params = {"page": page}
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("table.tbl_exchange tbody tr")

        if not rows:
            break

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 2:
                continue

            date_text = cols[0].text.strip()
            date = datetime.strptime(date_text, "%Y.%m.%d")

            if date < start_date:
                return pd.DataFrame(results)

            close_price = cols[1].text.strip().replace(",", "")
            results.append({
                "날짜": date,
                "종가": float(close_price)
            })

        page += 1

    return pd.DataFrame(results)
