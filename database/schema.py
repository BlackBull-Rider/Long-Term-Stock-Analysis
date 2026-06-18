# database/schema.py

from database.db import get_connection


def create_tables():

    conn = get_connection()

    cur = conn.cursor()

    # ==================================
    # MASTER STOCK TABLE
    # ==================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS stock_master(

        symbol TEXT PRIMARY KEY,

        company_name TEXT,

        sector TEXT,

        industry TEXT,

        market_cap REAL,

        listing_date TEXT

    )
    """)

    # ==================================
    # PRICE DATA
    # ==================================

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

    # ==================================
    # FUNDAMENTALS
    # ==================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS fundamentals(

        symbol TEXT PRIMARY KEY,

        pe REAL,

        pb REAL,

        roe REAL,

        roce REAL,

        sales_growth REAL,

        profit_growth REAL,

        debt_equity REAL,

        promoter REAL

    )
    """)

    # ==================================
    # PORTFOLIO
    # ==================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS portfolio(

        symbol TEXT PRIMARY KEY,

        qty INTEGER,

        avg_price REAL,

        invested REAL

    )
    """)

    # ==================================
    # TRANSACTIONS
    # ==================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,

        txn_type TEXT,

        qty INTEGER,

        price REAL,

        charges REAL,

        txn_date TEXT

    )
    """)

    conn.commit()

    conn.close()
