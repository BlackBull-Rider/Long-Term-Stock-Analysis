# data/fundamental_sync_v2.py

import pandas as pd
import yfinance as yf

from datetime import datetime

from database.db import get_connection


# ==========================
# GET SYMBOLS
# ==========================

def get_symbols():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT symbol
        FROM stock_master
        ORDER BY symbol
        """,
        conn
    )

    conn.close()

    return df["symbol"].tolist()


# ==========================
# SAVE
# ==========================

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

            data.get("promoter_holding"),

            data.get("institutional_holding"),

            data.get("fii_holding"),

            data.get("dii_holding"),

            data.get("free_cash_flow"),

            data.get("eps"),

            data.get("book_value"),

            data.get("dividend_yield"),

            datetime.now().isoformat()

        )
    )

    conn.commit()
    conn.close()


# ==========================
# FETCH
# ==========================

def fetch_fundamental(symbol):

    try:

        ticker = yf.Ticker(
            f"{symbol}.NS"
        )

        info = ticker.info

        if not info:

            return False

        roe = info.get(
            "returnOnEquity"
        )

        roe = (
            roe * 100
            if roe is not None
            else 0
        )

        sales_growth = info.get(
            "revenueGrowth"
        )

        sales_growth = (
            sales_growth * 100
            if sales_growth is not None
            else 0
        )

        profit_growth = info.get(
            "earningsGrowth"
        )

        profit_growth = (
            profit_growth * 100
            if profit_growth is not None
            else 0
        )

        institutional = info.get(
            "heldPercentInstitutions"
        )

        institutional = (
            institutional * 100
            if institutional is not None
            else 0
        )

        dividend = info.get(
            "dividendYield"
        )

        dividend = (
            dividend * 100
            if dividend is not None
            else 0
        )

        data = {

            "market_cap":
            info.get(
                "marketCap",
                0
            ),

            "pe":
            info.get(
                "trailingPE",
                0
            ),

            "pb":
            info.get(
                "priceToBook",
                0
            ),

            "roe":
            roe,

            "roce":
            roe,

            "debt_equity":
            info.get(
                "debtToEquity",
                0
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
                "freeCashflow",
                0
            ),

            "eps":
            info.get(
                "trailingEps",
                0
            ),

            "book_value":
            info.get(
                "bookValue",
                0
            ),

            "dividend_yield":
            dividend

        }

        save_fundamental(
            symbol,
            data
        )

        return True

    except Exception as e:

        print(
            f"FAILED : {symbol} | {e}"
        )

        return False


# ==========================
# RUN
# ==========================

def run_fundamental_scan(
    limit=None
):

    symbols = get_symbols()

    if limit:

        symbols = symbols[:limit]

    total = len(symbols)

    success = 0
    failed = 0

    print(
        f"\nScanning {total} Stocks...\n"
    )

    for index, symbol in enumerate(
        symbols,
        start=1
    ):

        print(
            f"[{index}/{total}] {symbol}"
        )

        ok = fetch_fundamental(
            symbol
        )

        if ok:

            success += 1

        else:

            failed += 1

    print("\n===================")

    print(
        f"Success : {success}"
    )

    print(
        f"Failed : {failed}"
    )

    print("===================\n")

    return success


if __name__ == "__main__":

    run_fundamental_scan()
