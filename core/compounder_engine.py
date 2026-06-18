# core/compounder_engine.py

import pandas as pd


def calculate_compounder_score(row):

    score = 0

    # ==========================
    # ROE
    # ==========================

    roe = row.get("roe", 0)

    if roe >= 30:
        score += 15

    elif roe >= 25:
        score += 12

    elif roe >= 20:
        score += 10

    elif roe >= 15:
        score += 5

    # ==========================
    # ROCE
    # ==========================

    roce = row.get("roce", 0)

    if roce >= 30:
        score += 15

    elif roce >= 25:
        score += 12

    elif roce >= 20:
        score += 10

    elif roce >= 15:
        score += 5

    # ==========================
    # DEBT
    # ==========================

    debt = row.get(
        "debt_equity",
        999
    )

    if debt <= 0.2:
        score += 15

    elif debt <= 0.5:
        score += 12

    elif debt <= 1:
        score += 8

    # ==========================
    # SALES GROWTH
    # ==========================

    sales = row.get(
        "sales_growth",
        0
    )

    if sales >= 25:
        score += 10

    elif sales >= 15:
        score += 7

    elif sales >= 10:
        score += 5

    # ==========================
    # PROFIT GROWTH
    # ==========================

    profit = row.get(
        "profit_growth",
        0
    )

    if profit >= 25:
        score += 10

    elif profit >= 15:
        score += 7

    elif profit >= 10:
        score += 5

    # ==========================
    # PROMOTER HOLDING
    # ==========================

    promoter = row.get(
        "promoter_holding",
        0
    )

    if promoter >= 70:
        score += 10

    elif promoter >= 60:
        score += 8

    elif promoter >= 50:
        score += 5

    # ==========================
    # INSTITUTIONAL
    # ==========================

    inst = row.get(
        "institutional_holding",
        0
    )

    if inst >= 25:
        score += 5

    elif inst >= 10:
        score += 3

    # ==========================
    # TECHNICAL TREND
    # ==========================

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

    if (
        cmp_price > ema50
        and
        ema50 > ema200
    ):
        score += 10

    return round(
        score,
        2
    )


def get_compounder_grade(score):

    if score >= 85:
        return "🏆 Elite Compounder"

    if score >= 70:
        return "🥇 A+ Compounder"

    if score >= 55:
        return "🥈 A Grade"

    if score >= 40:
        return "🥉 B Grade"

    return "⚠ Watchlist"


def enrich_compounder_dataframe(df):

    if df.empty:
        return df

    df = df.copy()

    df["Compounder Score"] = df.apply(
        calculate_compounder_score,
        axis=1
    )

    df["Grade"] = df[
        "Compounder Score"
    ].apply(
        get_compounder_grade
    )

    df = df.sort_values(
        by="Compounder Score",
        ascending=False
    )

    return df
