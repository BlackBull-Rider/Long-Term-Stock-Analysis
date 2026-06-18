# data/universe.py

import pandas as pd
import requests
import io

NSE_URL = (
    "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
)

def fetch_nse_universe():
    """
    Fetch all NSE EQ stocks
    """

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            NSE_URL,
            headers=headers,
            timeout=20
        )

        if response.status_code != 200:
            return pd.DataFrame()

        df = pd.read_csv(
            io.StringIO(response.text)
        )

        df.columns = (
            df.columns
            .str.strip()
        )

        df = df[
            df["SERIES"]
            .astype(str)
            .str.strip()
            == "EQ"
        ]

        return df

    except Exception as e:

        print(
            f"NSE Fetch Error: {e}"
        )

        return pd.DataFrame()


if __name__ == "__main__":

    universe = fetch_nse_universe()

    print(
        f"Loaded {len(universe)} NSE Stocks"
    )

    print(
        universe.head()
    )
