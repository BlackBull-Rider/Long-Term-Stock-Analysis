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

        macd REAL,

        macd_signal REAL,

        atr REAL,

        high52 REAL,

        low52 REAL,

        volume REAL,

        avg_volume REAL,

        updated_at TEXT

    )
    """)

    # ==========================
    # FUNDAMENTAL DATA
    # ==========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS fundamental_data(

        symbol TEXT PRIMARY KEY,

        market_cap REAL,

        pe REAL,

        pb REAL,

        roe REAL,

        roce REAL,

        debt_equity REAL,

        sales_growth REAL,

        profit_growth REAL,

        promoter_holding REAL,

        institutional_holding REAL,

        fii_holding REAL,

        dii_holding REAL,

        free_cash_flow REAL,

        eps REAL,

        book_value REAL,

        dividend_yield REAL,

        updated_at TEXT

    )
    """)

    # ==========================
    # IPO DATA
    # ==========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ipo_data(

        symbol TEXT PRIMARY KEY,

        company_name TEXT,

        listing_date TEXT,

        issue_price REAL,

        listing_price REAL,

        current_price REAL,

        gain_percent REAL,

        sales_growth REAL,

        profit_growth REAL,

        institutional_holding REAL,

        volume_ratio REAL,

        cmp REAL,

        ema20 REAL,

        ema50 REAL,

        ema200 REAL,

        rsi REAL,

        updated_at TEXT

    )
    """)

    # ==========================
    # PORTFOLIO
    # ==========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS portfolio(

        symbol TEXT PRIMARY KEY,

        qty REAL,

        avg_price REAL,

        invested REAL,

        current_value REAL,

        pnl REAL,

        pnl_percent REAL,

        updated_at TEXT

    )
    """)

    # ==========================
    # TRANSACTIONS
    # ==========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT,

        txn_type TEXT,

        qty REAL,

        price REAL,

        charges REAL,

        txn_date TEXT

    )
    """)

    # ==========================
    # WATCHLIST
    # ==========================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS watchlist(

        symbol TEXT PRIMARY KEY,

        notes TEXT,

        created_at TEXT

    )
    """)

    conn.commit()
    conn.close()
