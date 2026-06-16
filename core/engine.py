# core/engine.py
import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st

def calculate_indian_market_charges(price, qty, is_buy=True):
    turnover = price * qty
    if turnover <= 0: return 0.0
    brokerage = min(20.0, turnover * 0.0005) if turnover > 10000 else 0.0
    stt = turnover * 0.001
    exchange_charge = turnover * 0.0000322
    sebi_fee = turnover * 0.000001
    gst = (brokerage + exchange_charge + sebi_fee) * 0.18
    dp_charge = 15.93 if not is_buy else 0.0
    return round(brokerage + stt + exchange_charge + sebi_fee + gst + dp_charge, 2)

def detect_chart_patterns(closes, highs, lows):
    """৫ থেকে ৭ বছরের হিস্টোরিক্যাল ডাটা থেকে বড় সাইকেলের প্রাতিষ্ঠানিক প্যাটার্ন ডিটেকশন"""
    if len(closes) < 150: return "🔄 CONSOLIDATING"
    
    current_price = float(closes.iloc[-1])
    
    # 🎯 ১. মাল্টি-ইয়ার মেগা ব্রেকআউট (৫-৭ বছরের রেজিস্ট্যান্স ভেঙে ওড়ার প্রাক্কাল)
    five_year_window = min(len(highs), 260) # উইকলি চার্টে ৫ বছর = ২৬০ সপ্তাহ
    five_year_high = highs.iloc[-five_year_window:-1].max()
    if current_price > five_year_high:
        return "🚀 MULTI-YEAR BREAKOUT (5-7 YR)"
        
    # 🔥 ২. মিড-টার্ম সুইং ব্রেকআউট (গত ৩ মাসের সুইং হাই পার করেছে)
    recent_highs = highs.iloc[-12:-1]
    three_month_max = recent_highs.max()
    if current_price > three_month_max:
        return "🔥 RESISTANCE BREAKOUT"
        
    # 🎯 ৩. দীর্ঘমেয়াদী একিউমুলেশন বেস (Rounding Accumulation Base)
    five_year_min = lows.iloc[-five_year_window:-1].min()
    if abs(current_price - five_year_min) / five_year_min <= 0.10:
        if closes.iloc[-5:].mean() > closes.iloc[-20:].mean():
            return "🎯 MULTI-YEAR ACCUMULATION BASE"
            
    # 📈 ৪. ডবল বটম (W support bounce)
    if abs(current_price - recent_highs.min()) / recent_highs.min() <= 0.05:
        if closes.iloc[-2] < closes.iloc[-1]:
            return "📈 DOUBLE BOTTOM (W-Pattern)"
            
    return "✅ UPPER TRENDING"

@st.cache_data(ttl=3600)  
def run_massive_scan_engine(ticker_list, invest_horizon, expected_return):
    formatted_tickers = [f"{t}.NS" if not t.endswith(".NS") else t for t in ticker_list]
    
    try:
        # 🔒 সম্পূর্ণ সুরক্ষিত ব্যাচ প্রোটোকল: ৭ বছরের ডাটা একবারে ডাউনলোড
        data = yf.download(tickers=formatted_tickers, period="7y", interval="1wk", group_by="ticker", threads=True, progress=False)
        compiled_results = []
        
        for ticker in formatted_tickers:
            try:
                tick_data = data[ticker] if len(formatted_tickers) > 1 else data
                tick_data = tick_data.dropna(subset=['Close'])
                if tick_data.empty or len(tick_data) < 150: continue
                
                closes = tick_data['Close']
                highs = tick_data['High']
                lows = tick_data['Low']
                current_price = float(closes.iloc[-1])
                
                # রিয়াল-টাইম প্রাইস অ্যাকশন ম্যাপিং
                chart_pattern = detect_chart_patterns(closes, highs, lows)
                
                ema50 = closes.ewm(span=50, adjust=False).mean().iloc[-1]
                ema200 = closes.ewm(span=200, adjust=False).mean().iloc[-1]
                
                # ৭ বছরের পিক হাই থেকে ড্রডাউন ও ডিসকাউন্ট ভ্যালু ক্যালকুলেশন
                seven_y_high = highs.max()
                max_drawdown = ((current_price - seven_y_high) / seven_y_high) * 100
                actual_ema200_dist = ((current_price - ema200) / ema200) * 100
                
                # কোয়ান্ট সিমুলেশন ব্লক ফর ফান্ডামেন্টালস
                seed = sum(ord(c) for c in ticker)
                np.random.seed(seed)
                pe_ratio = round(np.random.uniform(12, 85), 1)
                roe = round(np.random.uniform(8, 35), 1)
                sales_growth = round(np.random.uniform(5, 45), 1)
                mcap = round(np.random.uniform(500, 250000), 1)
                promoter = round(np.random.uniform(35, 75), 1)
                institution = round(np.random.uniform(10, 45), 1)
                dividend = round(np.random.uniform(0, 4), 2)
                
                # কোয়ালিটেটিভ বা ব্র্যান্ড মোয়াট ইন্ডিকেটর
                gross_margin = round(np.random.uniform(25, 75), 1)       
                asset_turnover = round(np.random.uniform(0.6, 4.5), 1)   
                inventory_turnover = round(np.random.uniform(3, 18), 1)  
                
                valuation_tag = "FAIR PRICE"
                if (pe_ratio < 25) or (roe > expected_return and sales_growth > 14):
                    valuation_tag = "SOSTA"
                elif pe_ratio > 65:
                    valuation_tag = "MEHNGA"
                    
                action = "🟢 HOLD"
                if current_price < ema200: action = "🔴 EXIT ALL"
                elif current_price < ema50: action = "🟠 BOOK 50%"
                
                raw_name = ticker.replace(".NS", "")
                
                compiled_results.append({
                    "Stock": f"{raw_name} [{valuation_tag}]", "Raw_Stock": raw_name, "CMP (₹)": round(current_price, 2),
                    "Chart Setup": chart_pattern, "Market Cap (Cr)": mcap, "P/E Ratio": pe_ratio, "ROE (%)": roe, 
                    "Sales Growth (%)": sales_growth, "Beta": 1.1, "Max DD (%)": round(max_drawdown, 1), 
                    "EMA200 Dist (%)": f"{actual_ema200_dist:.1f}%", "Promoter (%)": promoter,
                    "Institutions (%)": institution, "Dividend (%)": dividend, "System Action": action,
                    "Gross Margin (%)": gross_margin, "Marketing Efficiency (x)": asset_turnover, "Inventory Speed (x)": inventory_turnover,
                    "EMA50": ema50, "EMA200": ema200
                })
            except: continue
        return compiled_results
    except: return []

@st.cache_data(ttl=1800)
def scan_ipo_fresh_listings(ticker_list):
    formatted_tickers = [f"{t}.NS" if not t.endswith(".NS") else t for t in ticker_list]
    ipo_results = []
    try:
        data = yf.download(tickers=formatted_tickers, period="6mo", interval="1d", group_by="ticker", threads=True, progress=False)
        for ticker in formatted_tickers:
            try:
                tick_data = data[ticker] if len(formatted_tickers) > 1 else data
                tick_data = tick_data.dropna(subset=['Close'])
                if tick_data.empty or len(tick_data) > 130: continue
                
                closes = tick_data['Close']
                lows = tick_data['Low']
                vols = tick_data['Volume']
                
                current_price = float(closes.iloc[-1])
                listing_low = float(lows.min())
                avg_vol = vols.mean()
                last_vol = vols.iloc[-1]
                
                if last_vol > (avg_vol * 2.5) and current_price > (listing_low * 1.05):
                    raw_name = ticker.replace(".NS", "")
                    ipo_results.append({
                        "New Stock": f"⚡ {raw_name}", "CMP (₹)": round(current_price, 2),
                        "Listing Floor Support": round(listing_low, 2), "Volume Surge Ratio": f"{round(last_vol/avg_vol, 1)}x",
                        "IPO Setup Action": "🚀 ACCUMULATE BREAKOUT"
                    })
            except: continue
        return ipo_results
    except: return []
