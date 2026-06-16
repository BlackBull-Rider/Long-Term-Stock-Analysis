import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

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
        stock = yf.Ticker(ticker)
        df = stock.history(period="2y", interval="1wk")
        if df.empty or len(df) < 50: return None
            
        current_price = df['Close'].iloc[-1]
        buy_price = holding_info["buy_price"]
        qty = holding_info["quantity"]
        
        current_return_p = ((current_price - buy_price) / buy_price) * 100
        invested_value = buy_price * qty
        current_value = current_price * qty
        pnl = current_value - invested_value
        
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['20_Week_High'] = df['High'].shift(1).rolling(window=20).max()
        
        ema_20 = df['EMA_20'].iloc[-1]
        ema_50 = df['EMA_50'].iloc[-1]
        twenty_week_high = df['20_Week_High'].iloc[-1]
        
        action = "🟢 HOLD & RIDE"
        if current_price < ema_50: action = "🔴 EMERGENCY EXIT"
        elif current_price < ema_20: action = "🟠 BOOK 50% QTY"
        elif current_price >= twenty_week_high: action = "🔥 RE-INVEST"

        return {
            "Stock": ticker.replace(".NS", ""),
            "Qty": int(qty),
            "Avg Buy (₹)": round(buy_price, 2),
            "CMP (₹)": round(current_price, 2),
            "Invested Value (₹)": round(invested_value, 2),
            "Current Value (₹)": round(current_value, 2),
            "Return (%)": round(current_return_p, 2),
            "P&L (₹)": round(pnl, 2),
            "System Action": action,
            "Book Qty": int(qty / 2) if "BOOK 50%" in action else (int(qty) if "EXIT" in action else 0),
            "Hold Qty": int(qty / 2) if "BOOK 50%" in action else (0 if "EXIT" in action else int(qty))
        }
    except:
        return None

# --- STREAMLIT UI ---
st.set_page_config(page_title="Institutional Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.title("🛡️ Institutional Portfolio & Risk Dashboard")
st.markdown("---")

results = []
for ticker, info in MY_HOLDINGS.items():
    data = track_advanced_portfolio(ticker, info)
    if data: results.append(data)

if results:
    final_df = pd.DataFrame(results)
    
    # ক্যালকুলেশনস
    total_invested = final_df["Invested Value (₹)"].sum()
    total_current = final_df["Current Value (₹)"].sum()
    total_pnl = final_df["P&L (₹)"].sum()
    total_return_p = (total_pnl / total_invested) * 100
    
    # ১. হাই-লেভেল ইনভেস্টর কার্ডস
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Invested", f"₹{total_invested:,.2f}")
    m2.metric("Current Value", f"₹{total_current:,.2f}")
    m3.metric("Net Profit / Loss", f"₹{total_pnl:,.2f}", f"{total_return_p:.2f}%")
    m4.metric("Active Tracked Stocks", str(len(final_df)))
    
    st.markdown("---")
    
    # ২. গ্রাফিকাল চার্ট সেকশন (Plotly Charts)
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📊 Portfolio Weight (কোথায় কত টাকা আছে)")
        fig_pie = px.pie(final_df, values='Current Value (₹)', names='Stock', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
        fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("💰 Stock-wise Profit / Loss")
        fig_bar = px.bar(final_df, x='Stock', y='P&L (₹)', text='P&L (₹)',
                         color='P&L (₹)', color_continuous_scale='RdYlGn')
        fig_bar.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.markdown("---")
    
    # ৩. মেইন লাইভ সিগন্যাল টেবিল
    st.subheader("📋 Live Technical Execution Signals")
    
    # সিগন্যাল হাইলাইট করার রুল
    def style_signals(df):
        co = pd.DataFrame('', index=df.index, columns=df.columns)
        for i, val in enumerate(df['System Action']):
            if "🔴" in val: co.iloc[i, df.columns.get_loc('System Action')] = 'background-color: #ff4d4d; color: white; font-weight: bold;'
            elif "🟠" in val: co.iloc[i, df.columns.get_loc('System Action')] = 'background-color: #ffa500; color: white; font-weight: bold;'
            elif "🔥" in val: co.iloc[i, df.columns.get_loc('System Action')] = 'background-color: #26a69a; color: white; font-weight: bold;'
            else: co.iloc[i, df.columns.get_loc('System Action')] = 'background-color: #2e7d32; color: white; font-weight: bold;'
        return co

    # ফাইনাল ক্লিন ডিসপ্লে টেবিল
    display_cols = ["Stock", "Qty", "Avg Buy (₹)", "CMP (₹)", "Return (%)", "P&L (₹)", "System Action", "Book Qty", "Hold Qty"]
    st.dataframe(final_df[display_cols].style.apply(style_signals, axis=None), use_container_width=True)
    
    st.success("ইনস্টিটিউশনাল অ্যালগরিদম সাকসেসফুলি রান করেছে। সমস্ত চার্ট এবং সিগন্যাল লাইভ।")
else:
    st.error("ডেটা ফেচ করা যায়নি।")
