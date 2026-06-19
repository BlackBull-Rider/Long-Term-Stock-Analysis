# core/stock_analysis_engine.py

import pandas as pd


def analyze_stock(row):

    result = {}

    score = 0

    # ==========================
    # FUNDAMENTAL ANALYSIS
    # ==========================

    roe = float(
        row.get(
            "roe",
            0
        )
    )

    roce = float(
        row.get(
            "roce",
            0
        )
    )

    debt = float(
        row.get(
            "debt_equity",
            999
        )
    )

    sales_growth = float(
        row.get(
            "sales_growth",
            0
        )
    )

    profit_growth = float(
        row.get(
            "profit_growth",
            0
        )
    )

    if roe >= 20:
        score += 20

    elif roe >= 15:
        score += 10

    if roce >= 20:
        score += 20

    elif roce >= 15:
        score += 10

    if debt <= 0.5:
        score += 15

    elif debt <= 1:
        score += 10

    if sales_growth >= 15:
        score += 15

    elif sales_growth >= 10:
        score += 8

    if profit_growth >= 15:
        score += 15

    elif profit_growth >= 10:
        score += 8

    # ==========================
    # TECHNICAL ANALYSIS
    # ==========================

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

    if cmp_price > ema200:
        score += 5

    if ema20 > ema50:
        score += 5

    if ema50 > ema200:
        score += 5

    if 50 <= rsi <= 70:
        score += 5

    # ==========================
    # FINAL DECISION
    # ==========================

    if score >= 80:

        action = "STRONG BUY"

    elif score >= 65:

        action = "BUY"

    elif score >= 50:

        action = "HOLD"

    else:

        action = "AVOID"

    # ==========================
    # TARGET PRICE
    # ==========================

    fair_value = cmp_price * (
        1 + (score / 100)
    )

    target_price = cmp_price * (
        1 + (score / 70)
    )

    # ==========================
    # RESULT
    # ==========================

    result["Score"] = round(
        score,
        2
    )

    result["Decision"] = action

    result["Fair Value"] = round(
        fair_value,
        2
    )

    result["Target Price"] = round(
        target_price,
        2
    )

    result["Risk"] = (

        "Low"

        if score >= 80

        else

        "Medium"

        if score >= 60

        else

        "High"

    )

    result["Reason"] = f"""

ROE = {roe}

ROCE = {roce}

Debt = {debt}

Sales Growth = {sales_growth}

Profit Growth = {profit_growth}

RSI = {rsi}

"""

    return result


def analyze_dataframe(df):

    if df.empty:

        return pd.DataFrame()

    rows = []

    for _, row in df.iterrows():

        analysis = analyze_stock(
            row
        )

        analysis["symbol"] = row.get(
            "symbol"
        )

        rows.append(
            analysis
        )

    return pd.DataFrame(
        rows
    )
