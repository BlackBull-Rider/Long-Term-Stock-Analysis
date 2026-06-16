import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# বাইরের ফাইল stocks.py থেকে ৫০০টি স্টকের লিস্ট ইম্পোর্ট
from stocks import SCREENER_WATCHLIST

# পেজ কনফিগারেশন (Bloomberg Dark theme look)
st.set_page_config(page_title="Alpha Institutional Terminal", layout="wide", initial_sidebar_state="collapsed")

# কাস্টম সিএসএস এরর ফিক্স করা হয়েছে (unsafe_allow_html=True ব্যবহার করে)
st.markdown("""
    <style>
    .metric-card {
        background-color: #111625;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #26a69a;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- গিটহাব সিক্রেট থেকে গুগল শিট লিংক অটো-লোড ---
sheet_url = None
try:
    sheet_url = st.secrets["public_gsheets_url"]
    # লিংকের শেষের ড্রাইভ ফরম্যাট ক্লিন করার লজিক
    if sheet_url and "?" in sheet_url:
        sheet_url = sheet_url.split("?")[0]
except:
    st.error("🚨 .streamlit/secrets.toml ফাইলে গুগল শিটের লিংক পাওয়া যায়নি!")

def load_portfolio_data():
    if not sheet_url:
        return pd.DataFrame(columns=["Stock", "Buy Price", "Quantity", "Date"])
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=sheet_url, ttl=0)
        if df.empty or "Stock" not in df.columns:
            return pd.DataFrame(columns=["Stock", "Buy Price", "Quantity", "Date"])
        return df
    except:
        return pd.DataFrame(columns=["Stock", "Buy Price", "Quantity", "Date"])

def save_portfolio_data(df):
    if sheet_url:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            conn.update(spreadsheet=sheet_url, data=df)
            return True
        except:
            return False
    return False

portfolio_df = load_portfolio_data()

# --- অ্যাডভান্সড ট্রেন্ড ও রিস্ক অ্যানালিসিস ইঞ্জিন ---
def analyze_stock_advanced(ticker, buy_price=None, qty=None):
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

        action = "🟢 STRONG BULL: HOLD"
        if current_price < ema_50: action = "🔴 TREND REVERSED: EXIT"
        elif current_price < ema_20: action = "🟠 MOMENTUM WEAK: BOOK 50%"
        elif current_price >= twenty_w_high: action = "🔥 BREAKOUT: RE-INVEST"
        
        data = {
            "Stock": ticker.replace(".NS", ""),
            "CMP (₹)": round(current_price, 2),
            "Market Cap (Cr)": round(market_cap, 2),
            "P/E Ratio": round(pe_ratio, 2) if pe_ratio else 0.0,
            "ROE (%)": round(roe, 2),
            "Sales Growth (%)": round(sales_growth, 2),
            "Beta": round(beta, 2) if beta else 1.0,
            "Max DD (%)": round(max_drawdown, 2),
            "Dist 20 EMA (%)": round(dist_20_ema, 2),
            "Dist 50 EMA (%)": round(dist_50_ema, 2),
            "System Action": action
        }
        
        if buy_price and qty:
            invested = buy_price * qty
            current_val = current_price * qty
            pnl = current_val - invested
            ret_p = (pnl / invested) * 100 if invested > 0 else 0
            data.update({
                "Qty": int(qty),
                "Avg Buy (₹)": round(buy_price, 2),
                "Invested (₹)": round(invested, 2),
                "Current Value (₹)": round(current_val, 2),
                "P&L (₹)": round(pnl, 2),
                "Return (%)": round(ret_p, 2),
                "Book Qty": int(qty / 2) if "BOOK 50%" in action else (int(qty) if "EXIT" in action else 0),
                "Hold Qty": int(qty / 2) if "BOOK 50%" in action else (0 if "EXIT" in action else int(qty))
            })
        return data
    except:
        return None

# --- নেভিগেশন ট্যাব ---
st.title("🦅 Alpha Institutional Investment Terminal")
tab1, tab2, tab3 = st.tabs(["🔍 Live Screener", "📥 Add Asset", "📊 Deep Portfolio Analysis"])

# TAB 1: SCREENER
with tab1:
    st.header("🎛️ Screener Core")
    col1, col2 = st.columns(2)
    min_sales = col1.slider("Min Sales Growth (%)", 0.0, 100.0, 15.0)
    min_roe = col1.slider("Min ROE (%)", 0.0, 100.0, 15.0)
    max_pe = col2.number_input("Max P/E Ratio", 0.0, 200.0, 40.0)
    min_mcap = col2.number_input("Min Market Cap (Cr)", 0.0, 10000.0, 500.0)
    
    if st.button("🔍 Execute Screen Scan"):
        progress = st.progress(0)
        results = []
        for index, ticker in enumerate(SCREENER_WATCHLIST[:30]): # দ্রুত স্ক্যানের জন্য ৩০টি টপ স্টক
            progress.progress((index + 1) / 30)
            res = analyze_stock_advanced(ticker)
            if res:
                if res["Sales Growth (%)"] >= min_sales and res["ROE (%)"] >= min_roe and res["Market Cap (Cr)"] >= min_mcap and (max_pe == 0 or res["P/E Ratio"] <= max_pe):
                    results.append(res)
        progress.empty()
        if results:
            st.dataframe(pd.DataFrame(results)[["Stock", "CMP (₹)", "Market Cap (Cr)", "P/E Ratio", "ROE (%)", "Sales Growth (%)", "System Action"]], use_container_width=True)

# TAB 2: ASSET INTAKE FORM
with tab2:
    st.header("📥 Asset Intake Form")
    with st.form("portfolio_form", clear_on_submit=True):
        stock_name = st.selectbox("🔍 Select Stock", options=sorted(SCREENER_WATCHLIST), index=None)
        buy_p = st.number_input("Buy Price (₹)", min_value=0.1)
        quantity = st.number_input("Quantity", min_value=1)
        buy_date = st.date_input("Date", datetime.now())
        if st.form_submit_button("➕ Link to Database") and sheet_url and stock_name:
            new_row = pd.DataFrame([{"Stock": stock_name, "Buy Price": buy_p, "Quantity": quantity, "Date": str(buy_date)}])
            if save_portfolio_data(pd.concat([portfolio_df, new_row], ignore_index=True)):
                st.success("Asset Synergized with Cloud Database!")
                st.rerun()

# TAB 3: DEEP PORTFOLIO ANALYSIS
with tab3:
    st.header("📊 Institutional Risk & Performance Analytics")
    if portfolio_df.empty:
        st.info("💡 Portfolio Database is vacant. Append assets from Tab 2.")
    else:
        with st.spinner("Calculating Portfolio Risk Analytics..."):
            port_results = []
            for _, row in portfolio_df.iterrows():
                res = analyze_stock_advanced(row["Stock"], float(row["Buy Price"]), int(row["Quantity"]))
                if res: port_results.append(res)
                
            if port_results:
                port_df = pd.DataFrame(port_results)
                
                t_invested = port_df["Invested (₹)"].sum()
                t_current = port_df["Current Value (₹)"].sum()
                t_pnl = port_df["P&L (₹)"].sum()
                t_ret = (t_pnl / t_invested) * 100 if t_invested > 0 else 0
                
                port_df["Weight"] = port_df["Current Value (₹)"] / t_current
                weighted_beta = (port_df["Beta"] * port_df["Weight"]).sum()
                weighted_pe = (port_df["P/E Ratio"] * port_df["Weight"]).sum()
                weighted_roe = (port_df["ROE (%)"] * port_df["Weight"]).sum()
                
                c_m1, c_m2, c_m3, c_m4 = st.columns(4)
                c_m1.metric("Total Capital Deployed", f"₹{t_invested:,.2f}")
                c_m2.metric("Current Assets Value", f"₹{t_current:,.2f}")
                c_m3.metric("Unrealized Net Alpha P&L", f"₹{t_pnl:,.2f}", f"{t_ret:.2f}%")
                c_m4.metric("Portfolio Beta (Risk Coefficient)", f"{weighted_beta:.2f}")
                
                st.markdown("---")
                
                col_c1, col_c2, col_c3 = st.columns(3)
                with col_c1:
                    st.plotly_chart(px.pie(port_df, values="Current Value (₹)", names="Stock", hole=0.5, title="Capital Allocation Matrix"), use_container_width=True)
                with col_c2:
                    st.plotly_chart(px.scatter(port_df, x="Beta", y="Return (%)", text="Stock", size="Qty", color="P&L (₹)", color_continuous_scale="RdYlGn", title="Risk vs Reward Scatter"), use_container_width=True)
                with col_c3:
                    st.plotly_chart(px.bar(port_df, x="Stock", y="Max DD (%)", color="Max DD (%)", color_continuous_scale="Reds_r", title="Max Drawdown Chart"), use_container_width=True)
                
                st.markdown("---")
                st.subheader("📋 Advanced Execution Metrics & Technical Buffer")
                
                display_terminal_cols = [
                    "Stock", "Qty", "Avg Buy (₹)", "CMP (₹)", "Return (%)", "P&L (₹)", 
                    "Beta", "Max DD (%)", "Dist 20 EMA (%)", "Dist 50 EMA (%)", 
                    "System Action", "Book Qty", "Hold Qty"
                ]
                st.dataframe(port_df[display_terminal_cols], use_container_width=True)
                st.info(f"💡 **Institutional Insight:** আপনার পোর্টফোলিওর Weighted P/E হলো **{weighted_pe:.2f}** এবং গড় ROE হলো **{weighted_roe:.2f}%**।")
