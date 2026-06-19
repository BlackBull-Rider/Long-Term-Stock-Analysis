# core/compounder_engine.py

import pandas as pd


def calculate_compounder_score(row):

    score = 0

    roe = float(
        row.get("roe", 0)
    )

    roce = float(
        row.get("roce", 0)
    )

    debt = float(
        row.get(
            "debt_equity",
            999
        )
    )

    sales = float(
        row.get(
            "sales_growth",
            0
        )
    )

    profit = float(
        row.get(
            "profit_growth",
            0
        )
    )

    promoter = float(
        row.get(
            "promoter_holding",
            0
        )
    )

    institutional = float(
        row.get(
            "institutional_holding",
            0
        )
    )

    cmp_price = float(
        row.get(
            "cmp",
            0
        )
    )

    ema20 = float(
        row.get(
            "ema20",
            0
        )
    )

    ema50 = float(
        row.get(
            "ema50",
            0
        )
    )

    ema200 = float(
        row.get(
            "ema200",
            0
        )
    )

    rsi = float(
        row.get(
            "rsi",
            0
        )
    )

    # ==========================
    # ROE
    # ==========================

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

    if debt <= 0.2:
        score += 15

    elif debt <= 0.5:
        score += 12

    elif debt <= 1:
        score += 8

    # ==========================
    # SALES GROWTH
    # ==========================

    if sales >= 25:
        score += 12

    elif sales >= 15:
        score += 8

    elif sales >= 10:
        score += 5

    # ==========================
    # PROFIT GROWTH
    # ==========================

    if profit >= 25:
        score += 12

    elif profit >= 15:
        score += 8

    elif profit >= 10:
        score += 5

    # ==========================
    # PROMOTER
    # ==========================

    if promoter >= 70:
        score += 10

    elif promoter >= 60:
        score += 8

    elif promoter >= 50:
        score += 5

    # ==========================
    # INSTITUTIONAL
    # ==========================

    if institutional >= 30:
        score += 10

    elif institutional >= 15:
        score += 6

    elif institutional >= 5:
        score += 3

    # ==========================
    # TREND
    # ==========================

    if (

        cmp_price > ema20

        and

        ema20 > ema50

        and

        ema50 > ema200

    ):

        score += 12

    # ==========================
    # RSI
    # ==========================

    if 55 <= rsi <= 70:

        score += 7

    return round(
        score,
        2
    )


def get_compounder_grade(score):

    if score >= 95:

        return "🟢 Elite Compounder"

    elif score >= 80:

        return "🟢 A+ Compounder"

    elif score >= 65:

        return "🟡 A Grade"

    elif score >= 50:

        return "🟠 B Grade"

    elif score >= 35:

        return "🔴 Watchlist"

    else:

        return "⛔ Avoid"


def enrich_compounder_dataframe(df):

    if df.empty:

        return df

    df = df.copy()

    df["Compounder Score"] = df.apply(
        calculate_compounder_score,
        axis=1
    )

    df["Compounder Grade"] = df[
        "Compounder Score"
    ].apply(
        get_compounder_grade
    )

    df = df.sort_values(
        by="Compounder Score",
        ascending=False
    )

    return df
