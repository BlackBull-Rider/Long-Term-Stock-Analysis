# stocks.py
import requests
import pandas as pd
import io
import streamlit as st

@st.cache_data(ttl=86400)
def get_live_nse_universe():
    """Direct exchange endpoint parsing via strict string-stripping protocol"""
    nse_url = "https://nearchives.nseindia.com/content/equities/EQUITY_L.csv"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        session = requests.Session()
        session.headers.update(headers)
        response = session.get(nse_url, timeout=15)
        
        if response.status_code == 200:
            csv_data = io.StringIO(response.text)
            df = pd.read_csv(csv_data)
            
            df.columns = df.columns.str.strip()
            if 'SERIES' in df.columns and 'SYMBOL' in df.columns:
                df['SERIES'] = df['SERIES'].astype(str).str.strip()
                df_eq = df[df['SERIES'] == 'EQ']
                symbols = df_eq['SYMBOL'].dropna().astype(str).str.strip().tolist()
                if len(symbols) > 100:
                    return symbols
    except Exception:
        pass
        
    # Reliable fallback database if NSE blocks request
    return [
        "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "BHARTIARTL",
        "LTIM", "ITC", "HINDUNILVR", "TATAMOTORS", "BAJFINANCE", "MARUTI",
        "TITAN", "ADANIENT", "JSWSTEEL", "TATASTEEL", "NTPC", "POWERGRID",
        "HAL", "BEL", "BHEL", "IRFC", "RVNL", "IRCON", "MAHABANK", "HUDCO",
        "ZOMATO", "JIOFIN", "SUZLON", "PAYTM", "LICI", "ADANIPOWER"
    ]

SCREENER_WATCHLIST = get_live_nse_universe()
