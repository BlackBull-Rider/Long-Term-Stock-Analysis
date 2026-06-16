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
        
        # পিওর পান্ডাস দিয়ে EMA ক্যালকুলেশন
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['20_Week_High'] = df['High'].shift(1).rolling(window=20).max()
        
        ema_20 = df['EMA_20'].iloc[-1]
        ema_50 = df['EMA_50'].iloc[-1]
        twenty_week_high = df['20_Week_High'].iloc[-1]
        
        # পিওর টেকনিক্যাল প্রফিট বুকিং এবং এন্ট্রি লজিক
        action = "📈 HOLD & RIDE"
        qty_to_book = 0
        qty_to_hold = qty
        
        # ১. যদি লং-টার্ম সাপোর্ট (50 EMA) ব্রেক হয় -> ফুল এক্সিট
        if current_price < ema_50:
            action = "🚨 EXIT ALL QTY"
            qty_to_book = qty
            qty_to_hold = 0
            
        # ২. যদি শর্ট-টার্ম মোমেন্টাম লাইন (20 EMA) ব্রেক হয় -> ৫০% প্রফিট বুক
        elif current_price < ema_20:
            action = "💰 BOOK 50% QTY"
            qty_to_book = round(qty / 2)
            qty_to_hold = qty - qty_to_book
            
        # ৩. যদি কারেন্ট প্রাইস ২০-উইক হাই ব্রেক করে ওপরে ওড়ে -> নতুন করে রি-ইনভেস্ট
        elif current_price >= twenty_week_high:
            action = "🔥 RE-INVEST"
            qty_to_book = 0
            qty_to_hold = qty

        return {
            "Stock": ticker.replace(".NS", ""),
            "Qty": int(qty),
            "Avg Buy": round(buy_price, 2),
            "CMP": round(current_price, 2),
            "Return": f"{round(current_return_p, 2)}%",
            "P&L": round(pnl, 2),
            "System Action": action,
            "Book Qty": int(qty_to_book),
            "Hold Qty": int(qty_to_hold),
            "20 EMA": round(ema_20, 2),
            "50 EMA": round(ema_50, 2)
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
            total_pnl = final_df["P&L"].sum()
            
            st.write("---")
            kpi1, kpi2 = st.columns(2)
            kpi1.metric(label="Total Portfolio Live P&L", value=f"Rs. {total_pnl:,.2f}")
            kpi2.metric(label="Total Tracked Assets", value=str(len(final_df)))
            st.write("---")
            
            # ডেটা ডিসপ্লে স্টেবিলিটি নিশ্চিত করতে স্ট্যান্ডার্ড ডেটাফ্রেম ভিউ
            st.dataframe(final_df, use_container_width=True)
            st.success("টেকনিক্যাল রুলস অনুযায়ী ড্যাশবোর্ড সফলভাবে আপডেট করা হয়েছে!")
        else:
            st.error("কোনো ডেটা পাওয়া যায়নি। অনুগ্রহ করে হোল্ডিং লিস্ট চেক করুন।")
