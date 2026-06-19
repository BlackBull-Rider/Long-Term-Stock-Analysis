# core/stock_score.py

def calculate_score(row):

    score = 0

    roe = row.get("roe", 0)
    roce = row.get("roce", 0)

    debt = row.get("debt_equity", 999)

    sales = row.get(
        "sales_growth",
        0
    )

    profit = row.get(
        "profit_growth",
        0
    )

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

    institutional = row.get(
        "institutional_holding",
        0
    )

    # ==========================
    # ROE
    # ==========================

    if roe >= 25:
        score += 15

    elif roe >= 20:
        score += 10

    elif roe >= 15:
        score += 5

    # ==========================
    # ROCE
    # ==========================

    if roce >= 25:
        score += 15

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
        score += 10

    elif debt <= 1:
        score += 5

    # ==========================
    # SALES GROWTH
    # ==========================

    if sales >= 25:
        score += 15

    elif sales >= 15:
        score += 10

    elif sales >= 10:
        score += 5

    # ==========================
    # PROFIT GROWTH
    # ==========================

    if profit >= 25:
        score += 15

    elif profit >= 15:
        score += 10

    elif profit >= 10:
        score += 5

    # ==========================
    # INSTITUTIONAL
    # ==========================

    if institutional >= 25:
        score += 10

    elif institutional >= 10:
        score += 5

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

        score += 15

    # ==========================
    # RSI
    # ==========================

    if 55 <= rsi <= 70:

        score += 10

    # ==========================
    # FINAL GRADE
    # ==========================

    if score >= 90:

        grade = "A+"

    elif score >= 75:

        grade = "A"

    elif score >= 60:

        grade = "B"

    elif score >= 45:

        grade = "C"

    else:

        grade = "D"

    return {

        "score": score,

        "grade": grade

    }
