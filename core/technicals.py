# core/technicals.py

import pandas as pd
import numpy as np


# ==========================
# EMA
# ==========================

def ema(series, period):

    return (
        series
        .ewm(
            span=period,
            adjust=False
        )
        .mean()
    )


# ==========================
# RSI
# ==========================

def calculate_rsi(
    close,
    period=14
):

    delta = close.diff()

    gain = delta.where(
        delta > 0,
        0
    )

    loss = -delta.where(
        delta < 0,
        0
    )

    avg_gain = (
        gain
        .rolling(period)
        .mean()
    )

    avg_loss = (
        loss
        .rolling(period)
        .mean()
    )

    rs = avg_gain / avg_loss

    rsi = (
        100
        -
        (
            100
            /
            (
                1 + rs
            )
        )
    )

    return rsi


# ==========================
# TECHNICAL SUMMARY
# ==========================

def calculate_technicals(df):

    result = {}

    close = df["Close"]

    result["cmp"] = round(
        float(close.iloc[-1]),
        2
    )

    result["ema20"] = round(
        float(
            ema(
                close,
                20
            ).iloc[-1]
        ),
        2
    )

    result["ema50"] = round(
        float(
            ema(
                close,
                50
            ).iloc[-1]
        ),
        2
    )

    result["ema200"] = round(
        float(
            ema(
                close,
                200
            ).iloc[-1]
        ),
        2
    )

    result["rsi"] = round(
        float(
            calculate_rsi(
                close
            ).iloc[-1]
        ),
        2
    )

    result["high52"] = round(
        float(
            df["High"].max()
        ),
        2
    )

    result["low52"] = round(
        float(
            df["Low"].min()
        ),
        2
    )

    result["avg_volume"] = round(
        float(
            df["Volume"]
            .tail(20)
            .mean()
        ),
        0
    )

    return result
