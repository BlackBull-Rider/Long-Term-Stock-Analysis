import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# পেজ সেটআপ
st.set_page_config(page_title="Alpha Institutional Hub", layout="wide")

# মেমোরিতে পোর্টফোলিও ডেটা সেভ রাখার জন্য
if "portfolio_db" not in st.session_state:
    st.session_state.portfolio_db = pd.DataFrame(columns=["Stock", "Buy Price", "Quantity", "Date"])

# --- ফাংশন: টেকনিক্যাল ও ফান্ডামেন্টাল অ্যানালিসিস ---
def analyze_stock(ticker, buy_price=None, qty=None):
    try:
        if not ticker.endswith(".NS"): ticker = f"{ticker}.NS"
        stock = yf.Ticker(ticker)
        
        # ১. হিস্টোরিক্যাল উইকলি ডেটা (টেকনিক্যাল)
        df = stock.history(period="2y", interval="1wk")
        if df.empty or len(df) < 50: return None
        
        current_price = df['Close'].iloc[-1]
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['20_W_High'] = df['High'].shift(1).rolling(window=20).max()
        
        ema_20 = df['EMA_20'].iloc[-1]
        ema_50 = df['EMA_50'].iloc[-1]
        twenty_w_high = df['20_W_High'].iloc[-1]
        
        # ২. লাইভ ফান্ডামেন্টাল ডেটা ফেচিং
        info = stock.info
        pe_ratio = info.get("trailingPE", 0)
        roe = info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0
        sales_growth_3y = info.get("revenueGrowth", 0) * 100 if info.get("revenueGrowth") else 0
        market_cap = info.get("marketCap", 0) / 10000000 # কোটিতে
        
        # সিগন্যাল লজিক
        action = "🟢 HOLD & RIDE"
        if current_price < ema_50: action = "🚨 EXIT ALL QTY"
        elif current_price < ema_20: action = "💰 BOOK 50% QTY"
        elif current_price >= twenty_w_high: action = "🔥 RE-INVEST"
        
        data = {
            "Stock": ticker.replace(".NS", ""),
            "CMP (₹)": round(current_price, 2),
            "Market Cap (Cr)": round(market_cap, 2),
            "P/E Ratio": round(pe_ratio, 2) if pe_ratio else 0.0,
            "ROE (%)": round(roe, 2),
            "Sales Growth (%)": round(sales_growth_3y, 2),
            "System Action": action,
            "20 EMA": round(ema_20, 2),
            "50 EMA": round(ema_50, 2)
        }
        
        if buy_price and qty:
            invested = buy_price * qty
            current_val = current_price * qty
            pnl = current_val - invested
            ret_p = (pnl / invested) * 100
            data.update({
                "Qty": qty,
                "Avg Buy (₹)": buy_price,
                "Invested (₹)": round(invested, 2),
                "Current Value (₹)": round(current_val, 2),
                "P&L (₹)": round(pnl, 2),
                "Return (%)": round(ret_p, 2)
            })
            
        return data
    except:
        return None

# --- নেভিগেশন ট্যাব ---
tab1, tab2, tab3 = st.tabs(["🔍 Live Fundamental Screener", "📥 Add Stock to Portfolio", "📊 Portfolio Analysis"])

# =========================================================================
# TAB 1: LIVE SCREENER WITH FILTER EDIT OPTION
# =========================================================================
with tab1:
    st.header("🦅 Custom Factor Screener & Parameter Query")
    st.write("Screener.in এর মতো এখানে আপনার নিজস্ব ফিল্টার প্যারামিটার এডিট করে রান করুন।")
    
    st.markdown("### 🎛️ Edit Filter Parameters (প্যারামিটার পরিবর্তন করুন)")
    
    # এডিটেবল প্যারামিটার অপশনস
    col1, col2 = st.columns(2)
    with col1:
        min_sales = st.slider("Minimum Sales Growth (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)
        min_roe = st.slider("Minimum ROE (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)
    with col2:
        max_pe = st.number_input("Maximum P/E Ratio (0 থেক ১০০ এর মধ্যে রাখুন, ০ মানে ইগনোর)", min_value=0.0, max_value=200.0, value=40.0, step=1.0)
        min_mcap = st.number_input("Minimum Market Cap (Cr)", min_value=0.0, value=500.0, step=100.0)

    # ব্যাকঅ্যান্ড স্ক্যানিং ওয়াচলিস্ট (তুমি চাইলে এখানে আরও নাম যোগ করতে পারো)
    SCREENER_WATCHLIST = ["TIPSINDLTD", "WAAREERTL", "SWARAJENG", "INGERRAND", "TATAMOTORS", "RELIANCE", "INFY", "SHILCHTECH", "CDSL", "HAL"]
    
    if st.button("🔍 Run Screen Query (সার্চ করুন)"):
        with st.spinner("আপনার দেওয়া ফিল্টার অনুযায়ী লাইভ মার্কেট স্ক্যান করা হচ্ছে..."):
            screened_results = []
            for ticker in SCREENER_WATCHLIST:
                res = analyze_stock(ticker)
                if res:
                    # ফিল্টার কন্ডিশন ম্যাচিং লজিক
                    cond_sales = res["Sales Growth (%)"] >= min_sales
                    cond_roe = res["ROE (%)"] >= min_roe
                    cond_mcap = res["Market Cap (Cr)"] >= min_mcap
                    cond_pe = True if max_pe == 0 or (res["P/E Ratio"] <= max_pe) else False
                    
                    if cond_sales and cond_roe and cond_mcap and cond_pe:
                        screened_results.append(res)
            
            if screened_results:
                screener_df = pd.DataFrame(screened_results)
                cols = ["Stock", "CMP (₹)", "Market Cap (Cr)", "P/E Ratio", "ROE (%)", "Sales Growth (%)", "System Action"]
                st.dataframe(screener_df[cols], use_container_width=True)
                st.success(f"📈 আপনার কাস্টম কোয়েরি সফলভাবে রান হয়েছে! {len(screener_df)} টি স্টক ফিল্টার পাস করেছে।")
            else:
                st.warning("⚠️ দুঃখিত! এই ফিল্টার প্যারামিটারে কোনো স্টক ম্যাচ করেনি। প্যারামিটার একটু কমিয়ে আবার ট্রাই করুন।")

# =========================================================================
# TAB 2: ADD STOCK TO PORTFOLIO
# =========================================================================
with tab2:
    st.header("📥 Add New Asset to Tracker")
    with st.form("portfolio_form", clear_on_submit=True):
        stock_name = st.text_input("Stock Ticker (যেমন: TATAMOTORS, TIPSINDLTD)").upper().strip()
        buy_p = st.number_input("Average Buy Price (₹)", min_value=0.1, step=0.1)
        quantity = st.number_input("Total Quantity", min_value=1, step=1)
        buy_date = st.date_input("Buying Date", datetime.now())
        
        submit_btn = st.form_submit_button("➕ Add Stock to My Portfolio")
        
        if submit_btn and stock_name:
            new_row = pd.DataFrame([{
                "Stock": stock_name, "Buy Price": buy_p, "Quantity": quantity, "Date": str(buy_date)
            }])
            st.session_state.portfolio_db = pd.concat([st.session_state.portfolio_db, new_row], ignore_index=True)
            st.success(f"{stock_name} সফলভাবে আপনার পোর্টফোলিওতে যোগ করা হয়েছে!")

# =========================================================================
# TAB 3: PORTFOLIO ANALYSIS
# =========================================================================
with tab3:
    st.header("📊 Real-Time Portfolio Technical Cockpit")
    
    if st.session_state.portfolio_db.empty:
        st.info("💡 আপনার পোর্টফোলিও এখন খালি। 'Add Stock' ট্যাব থেকে কিছু স্টক যোগ করুন।")
    else:
        with st.spinner("আপনার পোর্টফোলিওর স্টকগুলোর লাইভ চার্ট অ্যানালিসিস চলছে..."):
            port_results = []
            for _, row in st.session_state.portfolio_db.iterrows():
                res = analyze_stock(row["Stock"], row["Buy Price"], row["Quantity"])
                if res: port_results.append(res)
                
            if port_results:
                port_df = pd.DataFrame(port_results)
                
                t_invested = port_df["Invested (₹)"].sum()
                t_current = port_df["Current Value (₹)"].sum()
                t_pnl = port_df["P&L (₹)"].sum()
                t_ret = (t_pnl / t_invested) * 100 if t_invested > 0 else 0
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Invested", f"₹{t_invested:,.2f}")
                m2.metric("Current Value", f"₹{t_current:,.2f}")
                m3.metric("Net Live P&L", f"₹{t_pnl:,.2f}", f"{t_ret:.2f}%")
                
                st.markdown("---")
                
                c1, c2 = st.columns(2)
                with c1:
                    fig_p = px.pie(port_df, values="Current Value (₹)", names="Stock", hole=0.4, title="Portfolio Allocation")
                    st.plotly_chart(fig_p, use_container_width=True)
                with c2:
                    fig_b = px.bar(port_df, x="Stock", y="P&L (₹)", color="P&L (₹)", color_continuous_scale="RdYlGn", title="Stock-wise Profit/Loss")
                    st.plotly_chart(fig_b, use_container_width=True)
                    
                st.markdown("---")
                
                st.subheader("📋 Live Technical Signals & Action Plan")
                disp_cols = ["Stock", "Qty", "Avg Buy (₹)", "CMP (₹)", "Return (%)", "P&L (₹)", "System Action", "20 EMA", "50 EMA"]
                st.dataframe(port_df[disp_cols], use_container_width=True)
