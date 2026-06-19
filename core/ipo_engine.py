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


def ipo_quality_score(row):

    score = 0

    gain = row.get(
        "gain_percent",
        0
    )

    if gain >= 200:

        score += 25

    elif gain >= 100:

        score += 20

    elif gain >= 50:

        score += 15

    elif gain >= 20:

        score += 10

    institutional = row.get(
        "institutional_holding",
        0
    )

    if institutional >= 30:

        score += 15

    elif institutional >= 20:

        score += 10

    elif institutional >= 10:

        score += 5

    sales = row.get(
        "sales_growth",
        0
    )

    if sales >= 30:

        score += 15

    elif sales >= 20:

        score += 10

    elif sales >= 10:

        score += 5

    profit = row.get(
        "profit_growth",
        0
    )

    if profit >= 30:

        score += 15

    elif profit >= 20:

        score += 10

    elif profit >= 10:

        score += 5

    cmp_price = row.get(
        "cmp",
        0
    )

    ema20 = row.get(
        "ema20",
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

    if (

        cmp_price > ema20

        and

        ema20 > ema50

        and

        ema50 > ema200

    ):

        score += 20

    rsi = row.get(
        "rsi",
        0
    )

    if 55 <= rsi <= 75:

        score += 10

    return score


def ipo_grade(score):

    if score >= 80:

        return "🚀 Multibagger IPO"

    if score >= 65:

        return "🔥 Strong IPO"

    if score >= 50:

        return "🟢 Good IPO"

    if score >= 35:

        return "🟡 Watchlist"

    return "⚪ Weak"


def get_top_ipos():

    df = get_all_ipos()

    if df.empty:

        return df

    df = df.fillna(0)

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
