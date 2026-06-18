import pandas as pd
from datetime import datetime

from database.db import get_connection


def get_stock_options():

    conn = get_connection()

    query = """
    SELECT
        symbol,
        company_name
    FROM stock_master
    ORDER BY symbol
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    if df.empty:
        return []

    return [
        f"{row['symbol']} - {row['company_name']}"
        for _, row in df.iterrows()
    ]


def buy_stock(
    symbol,
    qty,
    price,
    charges=0
):

    conn = get_connection()
    cur = conn.cursor()

    invested = (qty * price) + charges

    existing = cur.execute(
        """
        SELECT *
        FROM portfolio
        WHERE symbol=?
        """,
        (symbol,)
    ).fetchone()

    if existing:

        old_qty = float(existing["qty"])
        old_avg = float(existing["avg_price"])

        new_qty = old_qty + qty

        new_avg = (
            (old_qty * old_avg)
            +
            (qty * price)
        ) / new_qty

        cur.execute(
            """
            UPDATE portfolio
            SET qty=?,
                avg_price=?,
                invested=?
            WHERE symbol=?
            """,
            (
                new_qty,
                new_avg,
                new_qty * new_avg,
                symbol
            )
        )

    else:

        cur.execute(
            """
            INSERT INTO portfolio(
                symbol,
                qty,
                avg_price,
                invested,
                current_value,
                pnl,
                pnl_percent,
                updated_at
            )
            VALUES(
                ?,?,?,?,?,?,?,?
            )
            """,
            (
                symbol,
                qty,
                price,
                invested,
                invested,
                0,
                0,
                datetime.now().isoformat()
            )
        )

    cur.execute(
        """
        INSERT INTO transactions(
            symbol,
            txn_type,
            qty,
            price,
            charges,
            txn_date
        )
        VALUES(
            ?,?,?,?,?,?
        )
        """,
        (
            symbol,
            "BUY",
            qty,
            price,
            charges,
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()


def sell_stock(
    symbol,
    qty,
    price,
    charges=0
):

    conn = get_connection()
    cur = conn.cursor()

    row = cur.execute(
        """
        SELECT *
        FROM portfolio
        WHERE symbol=?
        """,
        (symbol,)
    ).fetchone()

    if not row:

        conn.close()
        return

    current_qty = float(row["qty"])

    new_qty = current_qty - qty

    if new_qty <= 0:

        cur.execute(
            """
            DELETE FROM portfolio
            WHERE symbol=?
            """,
            (symbol,)
        )

    else:

        cur.execute(
            """
            UPDATE portfolio
            SET qty=?
            WHERE symbol=?
            """,
            (
                new_qty,
                symbol
            )
        )

    conn.commit()
    conn.close()


def get_portfolio():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM portfolio
        """,
        conn
    )

    conn.close()

    return df


def get_transactions():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM transactions
        ORDER BY txn_date DESC
        """,
        conn
    )

    conn.close()

    return df
