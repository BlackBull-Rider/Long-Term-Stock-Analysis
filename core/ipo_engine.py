# core/ipo_engine.py

import pandas as pd

from database.db import get_connection


def get_all_ipos():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM ipo_data
        """,
        conn
    )

    conn.close()

    return df


def ipo_gain_score(gain_percent):

    if gain_percent >= 300:
        return 25

    if gain_percent >= 200:
        return 20

    if gain_percent >= 100:
        return 15

    if gain_percent >= 50:
        return 10

    return 0


def revenue_score(growth):

    if growth >= 30:
        return 20

    if growth >= 20:
        return 15

    if growth >= 10:
        return 10

    return 0


def profit_score(growth):

    if growth >= 30:
        return 20

    if growth >= 20:
        return 15

    if growth >= 10:
        return 10

    return 0


def institutional_score(inst):

    if inst >= 30:
        return 15

    if inst >= 20:
        return 10

    if inst >= 10:
        return 5

    return 0


def technical_score(row):

    score = 0

    cmp_price = row.get(
        "cmp",
        0
    )

    ema50 = row.get(
        "ema50",
        0
    )

    ema200 = row.get(
        "ema200",
        0
    )

    rsi = row.get(
        "rsi",
        0
    )

    if (
        cmp_price > ema50
        and
        ema50 > ema200
    ):
        score += 10

    if 55 <= rsi <= 75:
        score += 10

    return score


def ipo_quality_score(row):

    score = 0

    score += ipo_gain_score(
        row.get(
            "gain_percent",
            0
        )
    )

    score += revenue_score(
        row.get(
            "sales_growth",
            0
        )
    )

    score += profit_score(
        row.get(
            "profit_growth",
            0
        )
    )

    score += institutional_score(
        row.get(
            "institutional_holding",
            0
        )
    )

    score += technical_score(
        row
    )

    return score


def ipo_grade(score):

    if score >= 80:
        return "🚀 IPO Multibagger"

    if score >= 65:
        return "🔥 High Potential"

    if score >= 50:
        return "🟢 Strong IPO"

    if score >= 35:
        return "🟡 Watchlist"

    return "🔴 Avoid"


def rank_ipos(df):

    if df.empty:
        return df

    df = df.copy()

    df["IPO Score"] = df.apply(
        ipo_quality_score,
        axis=1
    )

    df["IPO Grade"] = df[
        "IPO Score"
    ].apply(
        ipo_grade
    )

    df = df.sort_values(
        by="IPO Score",
        ascending=False
    )

    return df


def get_top_ipos():

    df = get_all_ipos()

    if df.empty:
        return df

    return rank_ipos(df)
