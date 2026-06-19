# core/screener.py

import pandas as pd

from database.db import get_connection

from core.compounder_engine import (
    calculate_compounder_score
)

from core.breakout_engine import (
    breakout_score
)

from core.institutional_tracker import (
    institutional_score
)


# ==========================
# LOAD DATA
# ==========================

def get_all_stocks():

    conn = get_connection()

    query = """

    SELECT

        t.*,

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
        f.dii_holding

    FROM technical_data t

    LEFT JOIN fundamental_data f

    ON t.symbol = f.symbol

    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    if df.empty:

        return df

    df = df.fillna(0)

    return df


# ==========================
# LONG TERM SCREENER
# ==========================

def long_term_screener():

    df = get_all_stocks()

    if df.empty:

        return df

    filtered = df[

        (df["roe"] >= 15)

        &

        (df["roce"] >= 15)

        &

        (df["debt_equity"] <= 1)

        &

        (df["sales_growth"] >= 10)

        &

        (df["profit_growth"] >= 10)

    ]

    filtered = filtered.copy()

    filtered["Compounder Score"] = filtered.apply(
        calculate_compounder_score,
        axis=1
    )

    return filtered.sort_values(
        by="Compounder Score",
        ascending=False
    )


# ==========================
# SWING SCREENER
# ==========================

def swing_screener():

    df = get_all_stocks()

    if df.empty:

        return df

    filtered = df[

        (df["cmp"] > df["ema20"])

        &

        (df["ema20"] > df["ema50"])

        &

        (df["ema50"] > df["ema200"])

        &

        (df["rsi"] >= 55)

    ]

    filtered = filtered.copy()

    filtered["Breakout Score"] = filtered.apply(
        breakout_score,
        axis=1
    )

    return filtered.sort_values(
        by="Breakout Score",
        ascending=False
    )


# ==========================
# 52W HIGH
# ==========================

def near_52w_high():

    df = get_all_stocks()

    if df.empty:

        return df

    filtered = df[

        df["cmp"]

        >=

        df["high52"] * 0.95

    ]

    return filtered.sort_values(
        by="rsi",
        ascending=False
    )


# ==========================
# COMPOUNDERS
# ==========================

def top_compounders():

    df = long_term_screener()

    if df.empty:

        return df

    return df.head(50)


# ==========================
# BREAKOUTS
# ==========================

def top_breakouts():

    df = swing_screener()

    if df.empty:

        return df

    return df.head(50)


# ==========================
# INSTITUTIONAL
# ==========================

def institutional_picks():

    df = get_all_stocks()

    if df.empty:

        return df

    df = df.copy()

    df["Institutional Score"] = df.apply(
        institutional_score,
        axis=1
    )

    return df.sort_values(
        by="Institutional Score",
        ascending=False
    ).head(50)
