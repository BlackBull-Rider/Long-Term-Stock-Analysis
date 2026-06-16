# core/engine.py
import yfinance as yf
import pandas as pd
import numpy as np

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

def analyze_stock_advanced(ticker, buy_price=None, qty=None, buy_charges=0.0):
    try:
        if not ticker.endswith(".NS"): ticker = f"{ticker}.NS"
        stock = yf.Ticker(ticker)
        df = stock.history(period="2y", interval="1wk")
        if df.empty or len(df) < 50: return None
        
        current_price = df['Close'].iloc[-1]
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['20_W_High'] = df['High'].shift(1).rolling(window=20).max()
        df['2y_High'] = df['High'].max()
        
        ema_20 = df['EMA_20'].iloc[-1]
        ema_50 = df['EMA_50'].iloc[-1]
        twenty_w_high = df['20_W_High'].iloc[-1]
        two_y_high = df['2y_High'].iloc[-1]
        
        dist_20_ema = ((current_price - ema_20) / ema_20) * 100
        dist_50_ema = ((current_price - ema_50) / ema_50) * 100
        max_drawdown = ((current_price - two_y_high) / two_y_high) * 100
        
        info = stock.info
        pe_ratio = info.get("trailingPE", 0)
        roe = info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0
        sales_growth = info.get("revenueGrowth", 0) * 100 if info.get("revenueGrowth") else 0
        market_cap = info.get("marketCap", 0) / 10000000 
        beta = info.get("beta", 1.0)

        action = "🟢 HOLD"
        if current_price < ema_50: action = "🔴 EXIT ALL"
        elif current_price < ema_20: action = "🟠 BOOK 50%"
        elif current_price >= twenty_w_high: action = "🔥 RE-INVEST"
        
        data = {
            "Stock": ticker.replace(".NS", ""), "CMP (₹)": round(current_price, 2),
            "Market Cap (Cr)": round(market_cap, 2), "P/E Ratio": round(pe_ratio, 2) if pe_ratio else 0.0,
            "ROE (%)": round(roe, 2), "Sales Growth (%)": round(sales_growth, 2), "Beta": round(beta, 2) if beta else 1.0,
            "Max DD (%)": round(max_drawdown, 2), "Dist 20 EMA (%)": round(dist_20_ema, 2),
            "Dist 50 EMA (%)": round(dist_50_ema, 2), "System Action": action
        }
        
        if buy_price and qty:
            invested = (buy_price * qty) + buy_charges
            current_val = current_price * qty
            est_sell_charges = calculate_indian_market_charges(current_price, qty, is_buy=False)
            pnl = (current_val - est_sell_charges) - invested
            ret_p = (pnl / invested) * 100 if invested > 0 else 0
            
            data.update({
                "Qty": int(qty), "Avg Buy (₹)": round(buy_price, 2), "Invested (₹)": round(invested, 2),
                "Current Value (₹)": round(current_val, 2), "Live Est Charges (₹)": round(est_sell_charges, 2),
                "Net P&L (₹)": round(pnl, 2), "Net Return (%)": round(ret_p, 2)
            })
        return data
    except:
        return None
