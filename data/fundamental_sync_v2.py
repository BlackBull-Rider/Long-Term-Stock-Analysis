# data/fundamental_sync_v2.py

import pandas as pd
import yfinance as yf
from datetime import datetime

from database.db import get_connection


def get_symbols():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT symbol
        FROM stock_master
        """,
        conn
    )

    conn.close()

    return df["symbol"].tolist()


def save_fundamental(symbol, data):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO fundamental_data(

            symbol,

            market_cap,
            pe,
            pb,

            roe,
            roce,

            debt_equity,

            sales_growth,
            profit_growth,

            promoter_holding,
            institutional_holding,

            fii_holding,
            dii_holding,

            free_cash_flow,

            eps,
            book_value,

            dividend_yield,

            updated_at

        )

        VALUES(
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
        """,
        (
            symbol,

            data["market_cap"],
            data["pe"],
            data["pb"],

            data["roe"],
            data["roce"],

            data["debt_equity"],

            data["sales_growth"],
            data["profit_growth"],

            data["promoter_holding"],
            data["institutional_holding"],

            data["fii_holding"],
            data["dii_holding"],

            data["free_cash_flow"],

            data["eps"],
            data["book_value"],

            data["dividend_yield"],

            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()


def fetch_fundamental(symbol):

    try:

        ticker = yf.Ticker(
            f"{symbol}.NS"
        )

        info = ticker.info

        roe = info.get(
            "returnOnEquity"
        )

        if roe is not None:
            roe = roe * 100

        sales_growth = info.get(
            "revenueGrowth"
        )

        if sales_growth is not None:
            sales_growth = sales_growth * 100

        profit_growth = info.get(
            "earningsGrowth"
        )

        if profit_growth is not None:
            profit_growth = profit_growth * 100

        institutional = info.get(
            "heldPercentInstitutions"
        )

        if institutional is not None:
            institutional = (
                institutional * 100
            )

        data = {

            "market_cap":
            info.get(
                "marketCap"
            ),

            "pe":
            info.get(
                "trailingPE"
            ),

            "pb":
            info.get(
                "priceToBook"
            ),

            "roe":
            roe,

            "roce":
            roe,

            "debt_equity":
            info.get(
                "debtToEquity"
            ),

            "sales_growth":
            sales_growth,

            "profit_growth":
            profit_growth,

            "promoter_holding":
            0,

            "institutional_holding":
            institutional,

            "fii_holding":
            0,

            "dii_holding":
            0,

            "free_cash_flow":
            info.get(
                "freeCashflow"
            ),

            "eps":
            info.get(
                "trailingEps"
            ),

            "book_value":
            info.get(
                "bookValue"
            ),

            "dividend_yield":
            info.get(
                "dividendYield"
            )

        }

        save_fundamental(
            symbol,
            data
        )

        return True

    except Exception as e:

        print(
            f"Error {symbol}: {e}"
        )

        return False


def run_fundamental_scan(
    limit=100
):

    symbols = get_symbols()

    success = 0

    total = min(
        len(symbols),
        limit
    )

    for i, symbol in enumerate(
        symbols[:limit],
        start=1
    ):

        print(
            f"[{i}/{total}] {symbol}"
        )

        ok = fetch_fundamental(
            symbol
        )

        if ok:
            success += 1

    return success


if __name__ == "__main__":

    result = run_fundamental_scan(
        limit=100
    )

    print(
        f"Updated {result} stocks"
    )
