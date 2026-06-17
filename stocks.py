# stocks.py
import requests
import pandas as pd
import io
import streamlit as st

@st.cache_data(ttl=86400)
def get_live_nse_universe():
    """Direct exchange endpoint parsing via corporate session bypass"""
    nse_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    
    # 🎯 BACKUP BULLETPROOF LAYER: যদি এনএসই মেইন সাইট ব্লক করে, তবে এই ওপেন সোর্স থেকে পুরো ২০০০+ লিস্ট একবারে রিড হবে
    backup_csv_url = "https://raw.githubusercontent.com/anirban-git/indian-stock-symbols/main/nse_symbols.csv"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    
    # মেথড ১: ডাইরেক্ট এনএসই মহাফেজখানা স্ক্র্যাপিং
    try:
        session = requests.Session()
        session.headers.update(headers)
        response = session.get(nse_url, timeout=12)
        
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            df.columns = df.columns.str.strip()
            if 'SERIES' in df.columns and 'SYMBOL' in df.columns:
                df_eq = df[df['SERIES'].astype(str).str.strip() == 'EQ']
                symbols = df_eq['SYMBOL'].dropna().astype(str).str.strip().tolist()
                if len(symbols) > 100:
                    return symbols
    except Exception:
        pass

    # 🚀 মেথড ২: আলটিমেট ব্যাকআপ (কোনো ৩২টা স্টকের লিমিটেশন নেই, পুরো ২০০০+ মেগা লিস্ট ডাইনামিকালি লোড হবে)
    try:
        res = requests.get(backup_csv_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=12)
        if res.status_code == 200:
            # যদি ব্যাকআপ ফাইলে ডাইরেক্ট কলাম থাকে
            df_back = pd.read_csv(io.StringIO(res.text))
            df_back.columns = df_back.columns.str.strip()
            
            # সম্ভাব্য কলাম নেম ফাইন্ডার (SYMBOL বা Ticker)
            target_col = None
            for col in ['SYMBOL', 'Symbol', 'symbol', 'ticker', 'Ticker']:
                if col in df_back.columns:
                    target_col = col
                    break
                    
            if target_col:
                symbols = df_back[target_col].dropna().astype(str).str.strip().tolist()
                if len(symbols) > 200:
                    return symbols
            else:
                # কলাম না মিললে ফার্স্ট কলামটাই টিকার হিসেবে নিয়ে নেবে
                symbols = df_back.iloc[:, 0].dropna().astype(str).str.strip().tolist()
                if len(symbols) > 200:
                    return symbols
    except Exception:
        pass
        
    # মেথড ৩: হার্ড ইমার্জেন্সি কোর ব্যাকআপ ইউনিভার্স (যদি ইন্টারনেট পুরো ক্র্যাশ করে)
    return [
        "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "BHARTIARTL", "LTIM", "ITC", 
        "HINDUNILVR", "TATAMOTORS", "BAJFINANCE", "MARUTI", "TITAN", "ADANIENT", "JSWSTEEL", 
        "TATASTEEL", "NTPC", "POWERGRID", "HAL", "BEL", "BHEL", "IRFC", "RVNL", "IRCON", 
        "MAHABANK", "HUDCO", "ZOMATO", "JIOFIN", "SUZLON", "PAYTM", "LICI", "ADANIPOWER",
        "WIPRO", "ONGC", "SUNPHARMA", "ADANIGREEN", "COALINDIA", "JINDALSTEL", "TATACOMM",
        "BPCL", "IOC", "GAIL", "HINDALCO", "VEDL", "EICHERMOT", "HEROMOTOCO", "BAJAJ-AUTO",
        "TECHM", "GRASIM", "ULTRACEMCO", "JSWENERGY", "SIEMENS", "ABB", "BEL", "TATAPOWER"
    ]

SCREENER_WATCHLIST = get_live_nse_universe()
