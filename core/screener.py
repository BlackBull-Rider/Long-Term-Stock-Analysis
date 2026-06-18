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

    if df.empty:
        return df

    # ==========================
    # TREND
    # ==========================

    def trend(row):

        if (
            row["cmp"] > row["ema20"]
            and
            row["ema20"] > row["ema50"]
            and
            row["ema50"] > row["ema200"]
        ):
            return "📈 Strong Uptrend"

        if (
            row["cmp"] > row["ema50"]
            and
            row["ema50"] > row["ema200"]
        ):
            return "🟢 Uptrend"

        if row["cmp"] > row["ema200"]:
            return "🟡 Recovery"

        return "🔴 Weak"

    # ==========================
    # BREAKOUT
    # ==========================

    def breakout(row):

        if row["cmp"] >= row["high52"]:
            return "🚀 52W Breakout"

        if row["cmp"] >= row["high52"] * 0.98:
            return "⚡ Near Breakout"

        return "⏸ Normal"

    # ==========================
    # VALUATION
    # ==========================

    def valuation(row):

        midpoint = (
            row["high52"]
            +
            row["low52"]
        ) / 2

        if row["cmp"] < midpoint * 0.8:
            return "🟢 Discount"

        if row["cmp"] > midpoint * 1.2:
            return "🟠 Premium"

        return "⚪ Fair"

    df["Trend"] = df.apply(
        trend,
        axis=1
    )

    df["Breakout"] = df.apply(
        breakout,
        axis=1
    )

    df["Valuation"] = df.apply(
        valuation,
        axis=1
    )

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

    return filtered.sort_values(
        by="rsi",
        ascending=False
    )


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

    return filtered.sort_values(
        by="rsi",
        ascending=False
    )
