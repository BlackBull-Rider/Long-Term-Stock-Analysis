# data/sync_engine.py

import yfinance as yf
import pandas as pd
from datetime import datetime

from database.db import get_connection
from core.technicals import calculate_technicals


def get_symbols():

    conn = get_connection()

    query = """
    SELECT symbol
    FROM stock_master
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df["symbol"].tolist()


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

    ))

    conn.commit()

    conn.close()


def scan_stock(symbol):

    try:

        ticker = yf.Ticker(
            f"{symbol}.NS"
        )

        df = ticker.history(
            period="1y"
        )

        if len(df) < 50:
            return False

        technicals = (
            calculate_technicals(df)
        )

        save_technicals(
            symbol,
            technicals
        )

        return True

    except Exception:

        return False


def run_scan(limit=50):

    symbols = get_symbols()

    completed = 0

    for symbol in symbols[:limit]:

        ok = scan_stock(symbol)

        if ok:

            completed += 1

    return completed
