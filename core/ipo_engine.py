# core/ipo_engine.py

import pandas as pd

from database.db import get_connection


# ==========================
# LOAD IPO DATA
# ==========================

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


# ==========================
# LISTING PERFORMANCE
# ==========================

def listing_score(gain_percent):

    if gain_percent >= 300:
        return 25

    elif gain_percent >= 200:
        return 20

    elif gain_percent >= 100:
        return 15

    elif gain_percent >= 50:
        return 10

    return 0


# ==========================
# REVENUE
# ==========================

def revenue_score(growth):

    if growth >= 40:
        return 20

    elif growth >= 25:
        return 15

    elif growth >= 15:
        return 10

    return 0


# ==========================
# PROFIT
# ==========================

def profit_score(growth):

    if growth >= 40:
        return 20

    elif growth >= 25:
        return 15

    elif growth >= 15:
        return 10

    return 0


# ==========================
# INSTITUTIONAL
# ==========================

def institutional_score(inst):

    if inst >= 40:
        return 15

    elif inst >= 25:
        return 10

    elif inst >= 10:
        return 5

    return 0


# ==========================
# VOLUME
# ==========================

def volume_score(volume_ratio):

    if volume_ratio >= 5:
        return 10

    elif volume_ratio >= 3:
        return 7

    elif volume_ratio >= 2:
        return 5

    return 0


# ==========================
# TECHNICAL
# ==========================

def technical_score(row):

    score = 0

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

    rsi = row.get(
        "rsi",
        0
    )

    if (

        cmp_price > ema20

        and

        ema20 > ema50

        and

        ema50 > ema200

    ):

        score += 10

    if 55 <= rsi <= 75:

        score += 10

    return score


# ==========================
# IPO QUALITY SCORE
# ==========================

def ipo_quality_score(row):

    score = 0

    score += listing_score(
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

    score += volume_score(
        row.get(
            "volume_ratio",
            0
        )
    )

    score += technical_score(
        row
    )

    return round(
        score,
        2
    )


# ==========================
# IPO GRADE
# ==========================

def ipo_grade(score):

    if score >= 85:

        return "🚀 Multibagger Candidate"

    elif score >= 70:

        return "🔥 High Potential"

    elif score >= 55:

        return "🟢 Strong IPO"

    elif score >= 40:

        return "🟡 Watchlist"

    else:

        return "🔴 Avoid"


# ==========================
# RANK IPOs
# ==========================

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


# ==========================
# TOP IPOs
# ==========================

def get_top_ipos():

    df = get_all_ipos()

    if df.empty:

        return df

    return rank_ipos(df).head(50)
