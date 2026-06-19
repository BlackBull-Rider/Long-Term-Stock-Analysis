# core/technicals.py

import pandas as pd
import numpy as np


# ==========================
# EMA
# ==========================

def ema(series, period):

    return series.ewm(
        span=period,
        adjust=False
    ).mean()


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

    avg_gain = gain.rolling(
        period
    ).mean()

    avg_loss = loss.rolling(
        period
    ).mean()

    rs = avg_gain / avg_loss

    rsi = (

        100

        -

        (

            100

            /

            (1 + rs)

        )

    )

    return rsi


# ==========================
# MACD
# ==========================

def calculate_macd(close):

    ema12 = ema(
        close,
        12
    )

    ema26 = ema(
        close,
        26
    )

    macd = ema12 - ema26

    signal = ema(
        macd,
        9
    )

    histogram = (
        macd - signal
    )

    return (

        macd.iloc[-1],

        signal.iloc[-1],

        histogram.iloc[-1]

    )


# ==========================
# ATR
# ==========================

def calculate_atr(
    df,
    period=14
):

    high_low = (

        df["High"]

        -

        df["Low"]

    )

    high_close = abs(

        df["High"]

        -

        df["Close"].shift()

    )

    low_close = abs(

        df["Low"]

        -

        df["Close"].shift()

    )

    ranges = pd.concat(

        [

            high_low,

            high_close,

            low_close

        ],

        axis=1

    )

    true_range = ranges.max(
        axis=1
    )

    atr = true_range.rolling(
        period
    ).mean()

    return atr.iloc[-1]


# ==========================
# TECHNICAL SUMMARY
# ==========================

def calculate_technicals(df):

    result = {}

    close = df["Close"]

    cmp_price = float(
        close.iloc[-1]
    )

    ema20 = float(
        ema(
            close,
            20
        ).iloc[-1]
    )

    ema50 = float(
        ema(
            close,
            50
        ).iloc[-1]
    )

    ema200 = float(
        ema(
            close,
            200
        ).iloc[-1]
    )

    rsi = float(
        calculate_rsi(
            close
        ).iloc[-1]
    )

    macd, signal, hist = (
        calculate_macd(
            close
        )
    )

    atr = calculate_atr(
        df
    )

    result["cmp"] = round(
        cmp_price,
        2
    )

    result["ema20"] = round(
        ema20,
        2
    )

    result["ema50"] = round(
        ema50,
        2
    )

    result["ema200"] = round(
        ema200,
        2
    )

    result["rsi"] = round(
        rsi,
        2
    )

    result["macd"] = round(
        float(macd),
        2
    )

    result["macd_signal"] = round(
        float(signal),
        2
    )

    result["macd_histogram"] = round(
        float(hist),
        2
    )

    result["atr"] = round(
        float(atr),
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

    result["trend"] = (

        "Bullish"

        if (

            cmp_price > ema20

            and

            ema20 > ema50

            and

            ema50 > ema200

        )

        else

        "Neutral"

    )

    return result
