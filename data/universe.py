# data/universe.py

import pandas as pd
import requests
import io


NSE_URL = (
    "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
)


def fetch_nse_universe():

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            NSE_URL,
            headers=headers,
            timeout=30
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

        # EQ only

        df = df[
            df["SERIES"]
            .astype(str)
            .str.strip()
            == "EQ"
        ]

        # Remove invalid symbols

        df = df[
            df["SYMBOL"]
            .notna()
        ]

        df = df.drop_duplicates(
            subset=["SYMBOL"]
        )

        df = df.sort_values(
            by="SYMBOL"
        )

        df = df.reset_index(
            drop=True
        )

        return df

    except Exception as e:

        print(
            f"NSE Fetch Error: {e}"
        )

        return pd.DataFrame()


if __name__ == "__main__":

    df = fetch_nse_universe()

    print(
        f"Loaded {len(df)} Stocks"
    )
