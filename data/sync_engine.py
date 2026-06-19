# data/sync_engine.py

import yfinance as yf
import pandas as pd

from datetime import datetime

from database.db import get_connection
from core.technicals import calculate_technicals


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
# SAVE TECHNICALS
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

            macd,
            macd_signal,

            atr,

            high52,
            low52,

            volume,
            avg_volume,

            updated_at

        )

        VALUES(
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
        """,
        (
            symbol,

            data.get("cmp"),

            data.get("ema20"),
            data.get("ema50"),
            data.get("ema200"),

            data.get("rsi"),

            data.get("macd"),
            data.get("macd_signal"),

            data.get("atr"),

            data.get("high52"),
            data.get("low52"),

            data.get("volume"),

            data.get("avg_volume"),

            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()


# ==========================
# SCAN STOCK
# ==========================

def scan_stock(symbol):

    try:

        ticker = yf.Ticker(
            f"{symbol}.NS"
        )

        df = ticker.history(

            period="2y",

            auto_adjust=True

        )

        if df.empty:

            return False

        if len(df) < 200:

            return False

        technicals = calculate_technicals(
            df
        )

        technicals["volume"] = float(
            df["Volume"].iloc[-1]
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
# RUN SCAN
# ==========================

def run_scan(limit=None):

    symbols = get_symbols()

    if limit:

        symbols = symbols[:limit]

    total = len(symbols)

    success = 0
    failed = 0

    print(
        f"\nStarting Scan : {total}\n"
    )

    for i, symbol in enumerate(

        symbols,

        start=1

    ):

        print(
            f"[{i}/{total}] {symbol}"
        )

        ok = scan_stock(
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


# ==========================
# TEST
# ==========================

if __name__ == "__main__":

    run_scan()
