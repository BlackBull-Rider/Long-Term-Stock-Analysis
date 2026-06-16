import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# বাইরের ফাইল stocks.py থেকে ৫০০টি স্টকের লিস্টটি ইম্পোর্ট করা হচ্ছে
from stocks import SCREENER_WATCHLIST

# পেজ সেটআপ
st.set_page_config(page_title="Alpha Institutional Hub", layout="wide")

# --- গুগল শিট ডেটাবেস কানেকশন ---
# ড্যাশবোর্ডের সাইডবারে ইউজারকে তার শিটের লিংক দেওয়ার অপশন দেওয়া হলো (সিকিউর প্রসেস)
st.sidebar.header("⚙️ Database Settings")
sheet_url = st.sidebar.text_input(
    "Google Sheet URLটি এখানে পেস্ট করুন:",
    placeholder="https://docs.google.com/spreadsheets/d/..."
)

# গুগল শিট থেকে ডেটা লোড করার ফাংশন
def load_portfolio_data():
    if not sheet_url:
        return pd.DataFrame(columns=["Stock", "Buy Price", "Quantity", "Date"])
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=sheet_url, ttl=0) # ttl=0 মানে প্রতিবার ফ্রেশ ডেটা আসবে
        # যদি শিট খালি থাকে বা কলাম না মেলে
        if df.empty or "Stock" not in df.columns:
            return pd.DataFrame(columns=["Stock", "Buy Price", "Quantity", "Date"])
        return df
    except:
        return pd.DataFrame(columns=["Stock", "Buy Price", "Quantity", "Date"])

# গুগল শিটে ডেটা সেভ করার ফাংশন
def save_portfolio_data(df):
    if sheet_url:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            conn.update(spreadsheet=sheet_url, data=df)
            return True
        except Exception as e:
            st.sidebar.error(f"Save Error: {e}")
            return False
    return False

# লাইভ ডাটাবেস লোড
portfolio_df = load_portfolio_data()

# --- ফাংশন: টেকনিক্যাল ও ফান্ডামেন্টাল অ্যানালিসিস ---
def analyze_stock(ticker, buy_price=None, qty=None):
    try:
        if not ticker.endswith(".NS"): ticker = f"{ticker}.NS"
        stock = yf.Ticker(ticker)
        df = stock.history(period="2y", interval="1wk")
        if df.empty or len(df) < 50: return None
        
        current_price = df['Close'].iloc[-1]
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['20_W_High'] = df['High'].shift(1).rolling(window=20).max()
        
        ema_20 = df['EMA_20'].iloc[-1]
        ema_50 = df['EMA_50'].iloc[-1]
        twenty_w_high = df['20_W_High'].iloc[-1]
        
        info = stock.info
        pe_ratio = info.get("trailingPE", 0)
        roe = info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0
        sales_growth_3y = info.get("revenueGrowth", 0) * 100 if info.get("revenueGrowth") else 0
        market_cap = info.get("marketCap", 0) / 10000000 
        
        action = "🟢 HOLD & RIDE"
        if current_price < ema_50: action = "🔴 EMERGENCY EXIT"
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
            ret_p = (pnl / invested) * 100 if invested > 0 else 0
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

# TAB 1: LIVE SCREENER
with tab1:
    st.header("🦅 Custom Factor Screener (Nifty 500 Watchlist)")
    st.markdown("### 🎛️ Edit Filter Parameters")
    col1, col2 = st.columns(2)
    with col1:
        min_sales = st.slider("Minimum Sales Growth (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)
        min_roe = st.slider("Minimum ROE (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)
    with col2:
        max_pe = st.number_input("Maximum P/E Ratio (0 means ignore)", min_value=0.0, max_value=200.0, value=40.0, step=1.0)
        min_mcap = st.number_input("Minimum Market Cap (Cr)", min_value=0.0, value=500.0, step=100.0)
    
    if st.button("🔍 Run Nifty 500 Scan"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        with st.spinner("স্ক্যান চলছে..."):
            screened_results = []
            total_stocks = len(SCREENER_WATCHLIST)
            for index, ticker in enumerate(SCREENER_WATCHLIST):
                progress_bar.progress((index + 1) / total_stocks)
                status_text.text(f"Scanning {index+1}/{total_stocks}: {ticker}")
                res = analyze_stock(ticker)
                if res:
                    if res["Sales Growth (%)"] >= min_sales and res["ROE (%)"] >= min_roe and res["Market Cap (Cr)"] >= min_mcap and (max_pe == 0 or res["P/E Ratio"] <= max_pe):
                        screened_results.append(res)
            progress_bar.empty()
            status_text.empty()
            if screened_results:
                st.dataframe(pd.DataFrame(screened_results)[["Stock", "CMP (₹)", "Market Cap (Cr)", "P/E Ratio", "ROE (%)", "Sales Growth (%)", "System Action"]], use_container_width=True)
            else:
                st.warning("⚠️ কোনো স্টক ম্যাচ করেনি।")

# TAB 2: ADD STOCK TO PORTFOLIO (গুগল শিটে রাইট করবে)
with tab2:
    st.header("📥 Add New Asset to Tracker")
    if not sheet_url:
        st.warning("⚠️ পোর্টফোলিও ফিচারটি সক্রিয় করতে প্রথমে বাঁদিকের সাইডবারে আপনার Google Sheet URLটি পেস্ট করুন!")
    
    with st.form("portfolio_form", clear_on_submit=True):
        stock_name = st.selectbox("🔍 Select/Search Stock Ticker", options=sorted(SCREENER_WATCHLIST), index=None, placeholder="Type stock letters...")
        buy_p = st.number_input("Average Buy Price (₹)", min_value=0.1, step=0.1)
        quantity = st.number_input("Total Quantity", min_value=1, step=1)
        buy_date = st.date_input("Buying Date", datetime.now())
        submit_btn = st.form_submit_button("➕ Add Stock to My Portfolio")
        
        if submit_btn and sheet_url:
            if not stock_name:
                st.error("⚠️ একটি স্টক সিলেক্ট করুন!")
            else:
                new_row = pd.DataFrame([{
                    "Stock": stock_name, "Buy Price": buy_p, "Quantity": quantity, "Date": str(buy_date)
                }])
                updated_portfolio = pd.concat([portfolio_df, new_row], ignore_index=True)
                if save_portfolio_data(updated_portfolio):
                    st.success(f"🎉 {stock_name} সফলভাবে Google Sheet ডেটাবেসে সেভ করা হয়েছে!")
                    st.rerun()

# TAB 3: PORTFOLIO ANALYSIS (গুগল শিট থেকে রিড করবে)
with tab3:
    st.header("📊 Real-Time Portfolio Technical Cockpit")
    if not sheet_url:
        st.info("💡 সাইডবারে Google Sheet URL পেস্ট করলেই আপনার রিয়েল পোর্টফোলিও অ্যানালিসিস এখানে লোড হবে।")
    elif portfolio_df.empty:
        st.info("💡 আপনার গুগল শিটটি এই মুহূর্তে খালি। ট্যাব ২ থেকে স্টক যোগ করুন।")
    else:
        with st.spinner("গুগল শিট থেকে ডেটা নিয়ে লাইভ চার্ট অ্যানালিসিস চলছে..."):
            port_results = []
            for _, row in portfolio_df.iterrows():
                res = analyze_stock(row["Stock"], float(row["Buy Price"]), int(row["Quantity"]))
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
                    st.plotly_chart(px.pie(port_df, values="Current Value (₹)", names="Stock", hole=0.4, title="Portfolio Allocation"), use_container_width=True)
                with c2:
                    st.plotly_chart(px.bar(port_df, x="Stock", y="P&L (₹)", color="P&L (₹)", color_continuous_scale="RdYlGn", title="Stock-wise Profit/Loss"), use_container_width=True)
                
                st.markdown("---")
                st.subheader("📋 Live Technical Signals & Action Plan")
                disp_cols = ["Stock", "Qty", "Avg Buy (₹)", "CMP (₹)", "Return (%)", "P&L (₹)", "System Action", "20 EMA", "50 EMA"]
                st.dataframe(port_df[disp_cols], use_container_width=True)
