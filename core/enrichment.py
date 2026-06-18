# core/enrichment.py

from core.patterns import (
    resistance_breakout,
    trend_status,
    valuation_tag
)


def enrich_dataframe(df):

    if df.empty:
        return df

    df = df.copy()

    df["Trend"] = df.apply(
        lambda x:
        trend_status(
            x["cmp"],
            x["ema20"],
            x["ema50"],
            x["ema200"]
        ),
        axis=1
    )

    df["Breakout"] = df.apply(
        lambda x:
        resistance_breakout(
            x["cmp"],
            x["high52"]
        ),
        axis=1
    )

    df["Valuation"] = df.apply(
        lambda x:
        valuation_tag(
            x["cmp"],
            x["high52"],
            x["low52"]
        ),
        axis=1
    )

    return df
