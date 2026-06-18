# core/smart_screener.py

import pandas as pd

from database.db import get_connection
from core.auto_parameters import generate_parameters


def load_data():

    conn = get_connection()

    query = """
    SELECT

        t.symbol,

        t.cmp,

        t.rsi,

        t.ema20,

        t.ema50,

        t.ema200,

        f.market_cap,

        f.pe,

        f.pb,

        f.roe,

        f.roce,

        f.debt_equity,

        f.sales_growth,

        f.profit_growth,

        f.promoter_holding,

        f.institutional_holding

    FROM technical_data t

    LEFT JOIN fundamental_data f

    ON t.symbol = f.symbol
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


def smart_screen(
    years,
    expected_return
):

    params = generate_parameters(
        years,
        expected_return
    )

    df = load_data()

    if df.empty:
        return df

    df = df.fillna(0)

    filtered = df[

        (df["roe"] >= params["roe"])

        &

        (df["roce"] >= params["roce"])

        &

        (df["debt_equity"] <= params["debt"])

        &

        (
            df["sales_growth"]
            >=
            params["sales_growth"]
        )

        &

        (
            df["profit_growth"]
            >=
            params["profit_growth"]
        )

        &

        (
            df["promoter_holding"]
            >=
            params["promoter"]
        )

    ]

    if filtered.empty:
        return filtered

    filtered["Score"] = (

        filtered["roe"]

        +

        filtered["roce"]

        +

        filtered["sales_growth"]

        +

        filtered["profit_growth"]

    )

    filtered = filtered.sort_values(
        by="Score",
        ascending=False
    )

    return filtered
