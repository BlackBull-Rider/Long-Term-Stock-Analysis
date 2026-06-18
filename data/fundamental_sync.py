# data/fundamental_sync.py

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


def save_fundamental(
    symbol,
    data
):

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

        data.get("market_cap"),

        data.get("pe"),

        data.get("pb"),

        data.get("roe"),

        data.get("roce"),

        data.get("debt_equity"),

        data.get("sales_growth"),

        data.get("profit_growth"),

        data.get("promoter"),

        data.get("institutional"),

        data.get("fii"),

        data.get("dii"),

        data.get("fcf"),

        data.get("eps"),

        data.get("book_value"),

        data.get("dividend_yield"),

        datetime.now().isoformat()

    ))

    conn.commit()
    conn.close()


def fetch_fundamental(symbol):

    try:

        ticker = yf.Ticker(
            f"{symbol}.NS"
        )

        info = ticker.info

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
            info.get(
                "returnOnEquity"
            ),

            "roce":
            None,

            "debt_equity":
            info.get(
                "debtToEquity"
            ),

            "sales_growth":
            info.get(
                "revenueGrowth"
            ),

            "profit_growth":
            info.get(
                "earningsGrowth"
            ),

            "promoter":
            None,

            "institutional":
            info.get(
                "heldPercentInstitutions"
            ),

            "fii":
            None,

            "dii":
            None,

            "fcf":
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

    except Exception:

        return False


def run_fundamental_scan(
    limit=50
):

    symbols = get_symbols()

    success = 0

    for symbol in symbols[:limit]:

        ok = fetch_fundamental(
            symbol
        )

        if ok:

            success += 1

    return success
