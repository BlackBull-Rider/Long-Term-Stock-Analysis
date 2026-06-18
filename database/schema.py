# database/schema.py

from database.db import get_connection


def create_tables():

    conn = get_connection()
    cur = conn.cursor()

    # ==========================
    # STOCK MASTER
    # ==========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS stock_master(

        symbol TEXT PRIMARY KEY,

        company_name TEXT,

        exchange TEXT,

        sector TEXT,

        industry TEXT,

        market_cap REAL,

        listing_date TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ==========================
    # MARKET DATA
    # ==========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS market_data(

        symbol TEXT PRIMARY KEY,

        cmp REAL,

        open REAL,

        high REAL,

        low REAL,

        volume REAL,

        updated_at TEXT

    )
    """)

    # ==========================
    # TECHNICAL DATA
    # ==========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS technical_data(

        symbol TEXT PRIMARY KEY,

        cmp REAL,

        ema20 REAL,

        ema50 REAL,

        ema200 REAL,

        rsi REAL,

        high52 REAL,

        low52 REAL,

        avg_volume REAL,

        updated_at TEXT

    )
    """)

    conn.commit()
    conn.close()
