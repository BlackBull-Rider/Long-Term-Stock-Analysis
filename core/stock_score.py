# core/stock_score.py

def calculate_score(row):

    score = 0

    # ROE

    if row["roe"] >= 25:
        score += 15

    elif row["roe"] >= 20:
        score += 10

    elif row["roe"] >= 15:
        score += 5

    # ROCE

    if row["roce"] >= 25:
        score += 15

    elif row["roce"] >= 20:
        score += 10

    elif row["roce"] >= 15:
        score += 5

    # Debt

    if row["debt_equity"] <= 0.2:
        score += 15

    elif row["debt_equity"] <= 0.5:
        score += 10

    elif row["debt_equity"] <= 1:
        score += 5

    # Sales Growth

    if row["sales_growth"] >= 25:
        score += 15

    elif row["sales_growth"] >= 15:
        score += 10

    elif row["sales_growth"] >= 10:
        score += 5

    # Profit Growth

    if row["profit_growth"] >= 25:
        score += 15

    elif row["profit_growth"] >= 15:
        score += 10

    elif row["profit_growth"] >= 10:
        score += 5

    # Trend

    if (
        row["cmp"] > row["ema20"]
        and
        row["ema20"] > row["ema50"]
        and
        row["ema50"] > row["ema200"]
    ):
        score += 15

    # RSI

    if 55 <= row["rsi"] <= 70:
        score += 10

    return score
