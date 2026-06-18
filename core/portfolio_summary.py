import pandas as pd


def portfolio_summary(df):

    if df.empty:

        return {

            "invested": 0,

            "current": 0,

            "pnl": 0,

            "return_pct": 0

        }

    invested = df["Invested"].sum()

    current = df["Current Value"].sum()

    pnl = current - invested

    if invested > 0:

        return_pct = (
            pnl / invested
        ) * 100

    else:

        return_pct = 0

    return {

        "invested": round(
            invested,
            2
        ),

        "current": round(
            current,
            2
        ),

        "pnl": round(
            pnl,
            2
        ),

        "return_pct": round(
            return_pct,
            2
        )

    }
