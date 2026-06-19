import pandas as pd

from database.db import get_connection


def load_recommendation_data():

    conn = get_connection()

    query = """

    SELECT

        t.symbol,

        t.cmp,
        t.rsi,

        t.ema20,
        t.ema50,
        t.ema200,

        t.high52,
        t.low52,

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

    INNER JOIN fundamental_data f

    ON t.symbol = f.symbol

    WHERE

        f.roe IS NOT NULL

        AND

        f.roce IS NOT NULL

        AND

        f.sales_growth IS NOT NULL

        AND

        f.profit_growth IS NOT NULL

    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    if df.empty:

        return df

    numeric_cols = [

        "cmp",

        "rsi",

        "ema20",
        "ema50",
        "ema200",

        "roe",
        "roce",

        "debt_equity",

        "sales_growth",
        "profit_growth",

        "institutional_holding"

    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    df = df.dropna()

    return df
