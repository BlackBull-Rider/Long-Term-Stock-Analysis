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
