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
# SAVE FUNDAMENTAL
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


# ==========================
# FETCH FUNDAMENTAL
# ==========================

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
            sales_growth = (
                sales_growth * 100
            )

        profit_growth = info.get(
            "earningsGrowth"
        )

        if profit_growth is not None:
            profit_growth = (
                profit_growth * 100
            )

        institutional = info.get(
            "heldPercentInstitutions"
        )

        if institutional is not None:
            institutional = (
                institutional * 100
            )

        dividend = info.get(
            "dividendYield"
        )

        if dividend is not None:
            dividend = dividend * 100

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

            # Yahoo ROCE দেয় না
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

            # Future source
            "promoter_holding":
            0,

            "institutional_holding":
            institutional,

            # Future source
            "fii_holding":
            0,

            # Future source
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
# FULL SCAN
# ==========================

def run_fundamental_scan(
    limit=None
):

    symbols = get_symbols()

    if limit is not None:

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

    print(
        "\n========================"
    )

    print(
        f"Success : {success}"
    )

    print(
        f"Failed  : {failed}"
    )

    print(
        "========================\n"
    )

    return success


# ==========================
# TEST
# ==========================

if __name__ == "__main__":

    run_fundamental_scan()
