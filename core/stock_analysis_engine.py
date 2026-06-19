
# core/stock_analysis_engine.py

import pandas as pd

from database.db import get_connection

from core.compounder_engine import (
    calculate_compounder_score
)

from core.breakout_engine import (
    breakout_score
)

from core.master_score import (
    master_score,
    master_grade
)


def get_stock_data(symbol):

    conn = get_connection()

    query = """

    SELECT

        t.symbol,

        t.cmp,
        t.ema20,
        t.ema50,
        t.ema200,

        t.rsi,

        t.high52,
        t.low52,

        t.avg_volume,

        f.market_cap,

        f.pe,
        f.pb,

        f.roe,
        f.roce,

        f.debt_equity,

        f.sales_growth,
        f.profit_growth,

        f.promoter_holding,
        f.institutional_holding,

        f.fii_holding,
        f.dii_holding,

        f.free_cash_flow,

        f.eps,
        f.book_value,

        f.dividend_yield

    FROM technical_data t

    LEFT JOIN fundamental_data f

    ON t.symbol = f.symbol

    WHERE t.symbol = ?

    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(symbol,)
    )

    conn.close()

    if df.empty:

        return None

    return df.iloc[0].to_dict()


def calculate_stock_analysis(data):

    compounder = (
        calculate_compounder_score(
            data
        )
    )

    breakout = (
        breakout_score(
            data
        )
    )

    institutional = 0

    ipo = 0

    data[
        "Compounder Score"
    ] = compounder

    data[
        "Breakout Score"
    ] = breakout

    data[
        "Institutional Score"
    ] = institutional

    data[
        "IPO Score"
    ] = ipo

    overall = master_score(
        data
    )

    grade = master_grade(
        overall
    )

    cmp_price = data.get(
        "cmp",
        0
    )

    target_price = round(

        cmp_price

        * 1.25,

        2

    )

    stoploss = round(

        cmp_price

        * 0.90,

        2

    )

    action = "HOLD"

    if overall >= 70:

        action = "BUY"

    elif overall < 40:

        action = "SELL"

    return {

        "symbol":
        data["symbol"],

        "cmp":
        cmp_price,

        "target":
        target_price,

        "stoploss":
        stoploss,

        "action":
        action,

        "overall":
        overall,

        "grade":
        grade,

        "compounder":
        compounder,

        "breakout":
        breakout,

        "roe":
        data.get(
            "roe",
            0
        ),

        "roce":
        data.get(
            "roce",
            0
        ),

        "debt":
        data.get(
            "debt_equity",
            0
        ),

        "sales":
        data.get(
            "sales_growth",
            0
        ),

        "profit":
        data.get(
            "profit_growth",
            0
        ),

        "rsi":
        data.get(
            "rsi",
            0
        )

    }


def analyze_stock(symbol):

    data = get_stock_data(
        symbol
    )

    if not data:

        return None

    return calculate_stock_analysis(
        data
    )
