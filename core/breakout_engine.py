# core/breakout_engine.py

import pandas as pd


def resistance_breakout(
    cmp_price,
    resistance
):

    if resistance <= 0:
        return False

    return cmp_price > resistance


def fifty_two_week_breakout(
    cmp_price,
    high52
):

    if high52 <= 0:
        return False

    return cmp_price >= high52


def volume_breakout(
    volume,
    avg_volume
):

    if avg_volume <= 0:
        return False

    return volume >= (
        avg_volume * 2
    )


def ema_breakout(
    cmp_price,
    ema20,
    ema50,
    ema200
):

    return (

        cmp_price > ema20

        and

        ema20 > ema50

        and

        ema50 > ema200

    )


def momentum_score(row):

    score = 0

    if row.get(
        "cmp",
        0
    ) > row.get(
        "ema20",
        0
    ):
        score += 20

    if row.get(
        "ema20",
        0
    ) > row.get(
        "ema50",
        0
    ):
        score += 20

    if row.get(
        "ema50",
        0
    ) > row.get(
        "ema200",
        0
    ):
        score += 20

    if row.get(
        "rsi",
        0
    ) >= 60:
        score += 20

    if row.get(
        "avg_volume",
        0
    ) > 0:
        score += 20

    return score


def breakout_score(row):

    score = 0

    if fifty_two_week_breakout(
        row.get("cmp", 0),
        row.get("high52", 0)
    ):
        score += 30

    if ema_breakout(
        row.get("cmp", 0),
        row.get("ema20", 0),
        row.get("ema50", 0),
        row.get("ema200", 0)
    ):
        score += 25

    if row.get(
        "rsi",
        0
    ) >= 60:
        score += 15

    score += (
        momentum_score(row) / 2
    )

    return round(
        score,
        2
    )


def breakout_grade(score):

    if score >= 80:
        return "🚀 Explosive"

    if score >= 65:
        return "🔥 Strong Breakout"

    if score >= 50:
        return "🟢 Breakout Candidate"

    if score >= 35:
        return "🟡 Watchlist"

    return "⚪ Normal"


def enrich_breakout(df):

    if df.empty:
        return df

    df = df.copy()

    df["Breakout Score"] = df.apply(
        breakout_score,
        axis=1
    )

    df["Breakout Grade"] = df[
        "Breakout Score"
    ].apply(
        breakout_grade
    )

    return df.sort_values(
        by="Breakout Score",
        ascending=False
    )
