# core/screener.py

import pandas as pd

from database.db import get_connection


def get_all_stocks():

    conn = get_connection()

    query = """
    SELECT *
    FROM technical_data
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


def breakout_candidates():

    df = get_all_stocks()

    if df.empty:
        return df

    filtered = df[

        (df["cmp"] > df["ema200"])

        &

        (df["rsi"] > 55)

    ]

    return filtered.sort_values(
        by="rsi",
        ascending=False
    )


def strong_uptrend():

    df = get_all_stocks()

    if df.empty:
        return df

    filtered = df[

        (df["cmp"] > df["ema20"])

        &

        (df["ema20"] > df["ema50"])

        &

        (df["ema50"] > df["ema200"])

    ]

    return filtered


def near_52w_high():

    df = get_all_stocks()

    if df.empty:
        return df

    filtered = df[

        (
            df["cmp"]
            >=
            df["high52"] * 0.95
        )

    ]

    return filtered
