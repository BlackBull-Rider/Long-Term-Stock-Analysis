# core/institutional_tracker.py

import pandas as pd


def fii_trend_score(current, previous):

    if current is None or previous is None:
        return 0

    change = current - previous

    if change >= 5:
        return 15

    if change >= 2:
        return 10

    if change > 0:
        return 5

    return 0


def dii_trend_score(current, previous):

    if current is None or previous is None:
        return 0

    change = current - previous

    if change >= 5:
        return 10

    if change >= 2:
        return 7

    if change > 0:
        return 3

    return 0


def promoter_trend_score(current, previous):

    if current is None or previous is None:
        return 0

    change = current - previous

    if change >= 2:
        return 20

    if change > 0:
        return 10

    if change < -2:
        return -15

    return 0


def pledge_score(pledge_percent):

    if pledge_percent is None:
        return 0

    if pledge_percent == 0:
        return 15

    if pledge_percent <= 5:
        return 10

    if pledge_percent <= 15:
        return 5

    return -20


def institutional_score(row):

    score = 0

    score += fii_trend_score(
        row.get("fii_current"),
        row.get("fii_previous")
    )

    score += dii_trend_score(
        row.get("dii_current"),
        row.get("dii_previous")
    )

    score += promoter_trend_score(
        row.get("promoter_current"),
        row.get("promoter_previous")
    )

    score += pledge_score(
        row.get("pledge_percent")
    )

    return score


def institutional_label(score):

    if score >= 40:
        return "🔥 Strong Accumulation"

    if score >= 25:
        return "🟢 Accumulation"

    if score >= 10:
        return "🟡 Neutral"

    return "🔴 Distribution"


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

    return df
