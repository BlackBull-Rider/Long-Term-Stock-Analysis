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

def analyze_stock_advanced(ticker, buy_price=None, qty=None, buy_charges=0.0, invest_horizon=1.5, expected_return=30.0):
    try:
        if not ticker.endswith(".NS"): ticker = f"{ticker}.NS"
        stock = yf.Ticker(ticker)
        df = stock.history(period="2y", interval="1wk")
        if df.empty or len(df) < 50: return None
        
        current_price = df['Close'].iloc[-1]
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['200_EMA'] = df['Close'].ewm(span=200, adjust=False).mean()
        df['2y_High'] = df['High'].max()
        
        ema50 = df['EMA_50'].iloc[-1]
        ema200 = df['200_EMA'].iloc[-1]
        two_y_high = df['2y_High'].iloc[-1]
        
        max_drawdown = ((current_price - two_y_high) / two_y_high) * 100
        actual_ema200_dist = ((current_price - ema200) / ema200) * 100
        
        # --- ইনস্টিটিউশনাল ফান্ডামেন্টাল ও ওনারশিপ এক্সট্রাকশন ---
        info = stock.info
        pe_ratio = info.get("trailingPE", 0)
        forward_pe = info.get("forwardPE", pe_ratio)
        roe = info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0.0
        sales_growth = info.get("revenueGrowth", 0) * 100 if info.get("revenueGrowth") else 0.0
        market_cap = info.get("marketCap", 0) / 10000000 
        beta = info.get("beta", 1.0)
        
        # ওনারশিপ এবং ডিভিডেন্ড ডেটা
        promoter_holding = info.get("heldPercentInsiders", 0.0) * 100 if info.get("heldPercentInsiders") else 0.0
        institution_holding = info.get("heldPercentInstitutions", 0.0) * 100 if info.get("heldPercentInstitutions") else 0.0
        dividend_yield = info.get("dividendYield", 0.0) * 100 if info.get("dividendYield") else 0.0
        peg_ratio = info.get("pegRatio", 1.0) if info.get("pegRatio") else 1.0

        # --- 🎯 ডাইনামিক ভ্যালুয়েশন ইঞ্জিন (সস্তা নাকি মহার্ঘ্য?) ---
        # PEG এবং P/E ম্যাট্রিক্সের সাথে হরাইজন ভিত্তিক গ্রোথ প্রজেকশন
        valuation_tag = "✅ FAIR PRICE"
        
        # যদি কোম্পানি আন্ডারভ্যালুড বা সস্তা হয়
        if (pe_ratio > 0 and pe_ratio < 25) or (peg_ratio > 0 and peg_ratio < 1.0):
            if roe > expected_return or sales_growth > 15:
                valuation_tag = "🔥 DISCOUNT / UNDERVALUED"
        # যদি অতিরিক্ত প্রিমিয়াম বা মহার্ঘ্য হয়
        elif pe_ratio > 60 or peg_ratio > 2.5:
            if invest_horizon < 2.0: # কম সময়ের জন্য বেশি দামি স্টক রিস্কি
                valuation_tag = "⚠️ PREMIUM / OVERVALUED"
        elif pe_ratio == 0:
            valuation_tag = "🚨 HIGH RISK (NO EARNINGS)"

        action = "🟢 HOLD"
        if current_price < ema200: action = "🔴 EXIT ALL"
        elif current_price < ema50: action = "🟠 BOOK 50%"
        
        raw_name = ticker.replace(".NS", "")
        display_name = f"{raw_name} [{valuation_tag}]"
        
        data = {
            "Stock": display_name, "Raw_Stock": raw_name, "CMP (₹)": round(current_price, 2),
            "Market Cap (Cr)": round(market_cap, 2), "P/E Ratio": round(pe_ratio, 2) if pe_ratio else 0.0,
            "ROE (%)": round(roe, 1), "Sales Growth (%)": round(sales_growth, 1), "Beta": round(beta, 2) if beta else 1.0,
            "Max DD (%)": round(max_drawdown, 1), "EMA200 Dist (%)": f"{actual_ema200_dist:.1f}%",
            "Promoter (%)": round(promoter_holding, 1) if promoter_holding > 0 else "N/A",
            "Institutions (%)": round(institution_holding, 1) if institution_holding > 0 else "N/A",
            "Dividend (%)": round(dividend_yield, 2), "System Action": action,
            "EMA50": ema50, "EMA200": ema200
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
