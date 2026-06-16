import streamlit as st
import yfinance as yf
import pandas as pd

# =========================================================================
# 📝 আপনার পোর্টফোলিও / হোল্ডিং লিস্ট 
# =========================================================================
MY_HOLDINGS = {
    "TIPSINDLTD.NS": {"buy_price": 450.00, "quantity": 100},
    "WAAREERTL.NS": {"buy_price": 1200.00, "quantity": 50},
    "SWARAJENG.NS": {"buy_price": 2100.00, "quantity": 30},
    "SHILCHTECH.NS": {"buy_price": 3500.00, "quantity": 20}
}

def track_advanced_portfolio(ticker, holding_info):
    try:
        # ২ বছরের উইকলি ডেটা ফেচ
        stock = yf.Ticker(ticker)
        df = stock.history(period="2y", interval="1wk")
        
        if df.empty or len(df) < 50:
            return None
            
        current_price = df['Close'].iloc[-1]
        buy_price = holding_info["buy_price"]
        qty = holding_info["quantity"]
        
        current_return_p = ((current_price - buy_price) / buy_price) * 100
        current_value = current_price * qty
        invested_value = buy_price * qty
        pnl = current_value - invested_value
        
        # পিওর পান্ডাস দিয়ে EMA ক্যালকুলেশন (No external library needed)
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['20_Week_High'] = df['High'].shift(1).rolling(window=20).max()
        
        ema_20 = df['EMA_20'].iloc[-1]
        ema_50 = df['EMA_50'].iloc[-1]
        twenty_week_high = df['20_Week_High'].iloc[-1]
        
        # পিওর টেকনিক্যাল প্রফিট বুকিং এবং এন্ট্রি লজিক
        action = "📈 STRONG BULL TREND: HOLD & RIDE"
        qty_to_book = 0
        qty_to_hold = qty
        
        # ১. যদি লং-টার্ম সাপোর্ট (50 EMA) ব্রেক হয় -> ফুল এক্সিট
        if current_price < ema_50:
            action = "🚨 TREND REVERSED: EXIT ALL QUANTITY"
            qty_to_book = qty
            qty_to_hold = 0
            
        # ২. যদি শর্ট-টার্ম মোমেন্টাম লাইন (20 EMA) ব্রেক হয় -> ৫০% প্রফিট বুক
        elif current_price < ema_20:
            action = "💰 MOMENTUM WEAK: BOOK 50% QUANTITY"
            qty_to_book = round(qty / 2)
            qty_to_hold = qty - qty_to_book
            
        # ৩. যদি কারেন্ট প্রাইস ২০-উইক হাই ব্রেক করে ওপরে ওড়ে -> নতুন করে রি-ইনভেস্ট
        elif current_price >= twenty_week_high:
            action = "🔥 BREAKOUT: HOLD / RE-INVEST ALLOWED"
            qty_to_book = 0
            qty_to_hold = qty

        return {
            "Stock": ticker.replace(".NS", ""),
            "Qty": qty,
            "Avg Buy (Rs.)": round(buy_price, 2),
            "CMP (Rs.)": round(current_price, 2),
            "Return (%)": f"{round(current_return_p, 2)}%",
            "P&L (Rs.)": round(pnl, 2),
            "System Action": action,
            "Book Qty": qty_to_book,
            "Hold Qty": qty_to_hold,
            "20 EMA (Partial Booking)": round(ema_20, 2) if not pd.isna(ema_20) else "N/A",
            "50 EMA (Full Exit Line)": round(ema_50, 2) if not pd.isna(ema_50) else "N/A"
        }
    except Exception as e:
        return None

# --- STREAMLIT UI ---
st.set_page_config(page_title="Advanced Institutional System", layout="wide")
st.title("🛡️ Institutional Technical Tracking & Execution Dashboard")
st.subheader("Pure Technical Profit Booking | Anti-Emotion Execution")

if st.button("🔄 Scan & Track Portfolio Live"):
    with st.spinner("লাইভ মার্কেট চার্ট এবং ইএমএ লাইন স্ক্যান করা হচ্ছে..."):
        results = []
        for ticker, info in MY_HOLDINGS.items():
            data = track_advanced_portfolio(ticker, info)
            if data:
                results.append(data)
                
        if results:
            final_df = pd.DataFrame(results)
            total_pnl = final_df["P&L (Rs.)"].sum()
            
            st.write("---")
            kpi1, kpi2 = st.columns(2)
            kpi1.metric(label="Total Portfolio Live P&L", value=f"Rs. {total_pnl:,.2f}")
            kpi2.metric(label="Total Tracked Assets", value=str(len(final_df)))
            st.write("---")
            
            def highlight_action(val):
                if "BOOK 50%" in val:
                    return 'background-color: #e67e22; color: white; font-weight: bold;'
                elif "EXIT" in val:
                    return 'background-color: #e74c3c; color: white; font-weight: bold;'
                elif "RE-INVEST" in val:
                    return 'background-color: #2ecc71; color: white; font-weight: bold;'
                return 'background-color: #2c3e50; color: #ecf0f1;'

            st.dataframe(
                final_df.style.applymap(highlight_action, subset=['System Action']),
                use_container_width=True
            )
            st.success("টেকনিক্যাল রুলস অনুযায়ী ড্যাশবোর্ড আপডেট করা হয়েছে!")
        else:
            st.error("কোনো ডেটা পাওয়া যায়নি। অনুগ্রহ করে হোল্ডিং লিস্ট চেক করুন।")
