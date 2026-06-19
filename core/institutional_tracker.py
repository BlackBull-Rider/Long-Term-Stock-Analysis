# core/institutional_tracker.py

import pandas as pd


# ==========================
# FII TREND
# ==========================

def fii_trend_score(
    current,
    previous
):

    if current is None or previous is None:

        return 0

    change = current - previous

    if change >= 5:

        return 20

    elif change >= 2:

        return 15

    elif change > 0:

        return 10

    elif change < -5:

        return -15

    return 0


# ==========================
# DII TREND
# ==========================

def dii_trend_score(
    current,
    previous
):

    if current is None or previous is None:

        return 0

    change = current - previous

    if change >= 5:

        return 15

    elif change >= 2:

        return 10

    elif change > 0:

        return 5

    elif change < -5:

        return -10

    return 0


# ==========================
# PROMOTER TREND
# ==========================

def promoter_trend_score(
    current,
    previous
):

    if current is None or previous is None:

        return 0

    change = current - previous

    if change >= 3:

        return 25

    elif change > 0:

        return 15

    elif change <= -3:

        return -20

    elif change < 0:

        return -10

    return 0


# ==========================
# PLEDGE
# ==========================

def pledge_score(
    pledge_percent
):

    if pledge_percent is None:

        return 0

    if pledge_percent == 0:

        return 20

    elif pledge_percent <= 5:

        return 15

    elif pledge_percent <= 10:

        return 10

    elif pledge_percent <= 20:

        return 5

    return -25


# ==========================
# INSTITUTIONAL SCORE
# ==========================

def institutional_score(row):

    score = 0

    score += fii_trend_score(

        row.get(
            "fii_current"
        ),

        row.get(
            "fii_previous"
        )

    )

    score += dii_trend_score(

        row.get(
            "dii_current"
        ),

        row.get(
            "dii_previous"
        )

    )

    score += promoter_trend_score(

        row.get(
            "promoter_current"
        ),

        row.get(
            "promoter_previous"
        )

    )

    score += pledge_score(

        row.get(
            "pledge_percent"
        )

    )

    return round(
        score,
        2
    )


# ==========================
# LABEL
# ==========================

def institutional_label(score):

    if score >= 50:

        return "🔥 Heavy Accumulation"

    elif score >= 35:

        return "🟢 Strong Accumulation"

    elif score >= 20:

        return "🟡 Accumulation"

    elif score >= 0:

        return "⚪ Neutral"

    else:

        return "🔴 Distribution"


# ==========================
# DATAFRAME ENRICHMENT
# ==========================

def enrich_institutional(df):

    if df.empty:

        return df

    df = df.copy()

    df["Institutional Score"] = df.apply(
        institutional_score,
        axis=1
    )

    df["Institutional Trend"] = df[
        "Institutional Score"
    ].apply(
        institutional_label
    )

    return df.sort_values(
        by="Institutional Score",
        ascending=False
    )
