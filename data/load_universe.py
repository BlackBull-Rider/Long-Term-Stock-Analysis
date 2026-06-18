# data/load_universe.py

from database.db import get_connection
from data.universe import fetch_nse_universe


def load_nse_universe():

    df = fetch_nse_universe()

    if df.empty:
        return 0

    conn = get_connection()
    cur = conn.cursor()

    inserted = 0

    for _, row in df.iterrows():

        symbol = str(row["SYMBOL"]).strip()
        company = str(row["NAME OF COMPANY"]).strip()

        cur.execute(
            """
            INSERT OR REPLACE INTO stock_master(
                symbol,
                company_name,
                exchange
            )
            VALUES (?, ?, ?)
            """,
            (
                symbol,
                company,
                "NSE"
            )
        )

        inserted += 1

    conn.commit()
    conn.close()

    return inserted
