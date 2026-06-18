# data/sync_engine.py

import yfinance as yf
import pandas as pd

from datetime import datetime

from database.db import get_connection
from core.technicals import calculate_technicals


# ==========================
# GET ALL SYMBOLS
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
# SAVE TECHNICAL DATA
# ==========================

def save_technicals(
    symbol,
    data
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO technical_data(

            symbol,

            cmp,

            ema20,
            ema50,
            ema200,

            rsi,

            high52,
            low52,

            avg_volume,

            updated_at

        )

        VALUES(
            ?,?,?,?,?,?,?,?,?,?
        )
        """,
        (
            symbol,

            data["cmp"],

            data["ema20"],
            data["ema50"],
            data["ema200"],

            data["rsi"],

            data["high52"],
            data["low52"],

            data["avg_volume"],

            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()


# ==========================
# SCAN SINGLE STOCK
# ==========================

def scan_stock(symbol):

    try:

        ticker = yf.Ticker(
            f"{symbol}.NS"
        )

        df = ticker.history(
            period="1y",
            auto_adjust=True
        )

        if df.empty:
            return False

        if len(df) < 200:
            return False

        technicals = calculate_technicals(
            df
        )

        save_technicals(
            symbol,
            technicals
        )

        return True

    except Exception as e:

        print(
            f"FAILED : {symbol} | {e}"
        )

        return False


# ==========================
# FULL MARKET SCAN
# ==========================

def run_scan(limit=None):

    symbols = get_symbols()

    if limit is not None:

        symbols = symbols[:limit]

    total = len(symbols)

    completed = 0
    failed = 0

    print(
        f"\nStarting Scan : {total} Stocks\n"
    )

    for index, symbol in enumerate(
        symbols,
        start=1
    ):

        print(
            f"[{index}/{total}] {symbol}"
        )

        ok = scan_stock(
            symbol
        )

        if ok:

            completed += 1

        else:

            failed += 1

    print("\n====================")

    print(
        f"Success : {completed}"
    )

    print(
        f"Failed  : {failed}"
    )

    print("====================\n")

    return completed


# ==========================
# TEST
# ==========================

if __name__ == "__main__":

    run_scan()
