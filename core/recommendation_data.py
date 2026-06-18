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
