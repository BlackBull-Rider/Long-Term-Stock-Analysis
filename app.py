# app.py
import streamlit as st
import pandas as pd
import requests
import base64
import io
from datetime import datetime
import yfinance as yf
import plotly.express as px

# 🎯 ১. সেশন স্টেট মেমোরি সবার আগে ব্যাকবোন হিসেবে লক করা হলো
if "live_logs" not in st.session_state:
    st.session_state.live_logs = []

from stocks import SCREENER_WATCHLIST
from core.styles import apply_terminal_theme, render_branding_header, render_operational_guidelines, render_terminal_footer
from core.engine import (
    calculate_indian_market_charges, run_offline_sync_pipeline, 
    load_offline_market_data, add_log
)

# Premium UI Dark HUD Rules Apply
apply_terminal_theme()
render_branding_header()

# =========================================================================
# GITHUB ARCHITECTURE SETTINGS
# =========================================================================
GITHUB_USER = "BlackBull-Rider"  
GITHUB_REPO = "Long-Term-Stock-Analysis"  

if "MY_GITHUB_TOKEN" in st.secrets:
    GITHUB_TOKEN = st.secrets["MY_GITHUB_TOKEN"]
    g_token_str = str(GITHUB_TOKEN).strip()
    masked_token = f"{g_token_str[:6]}...{g_token_str[-4:]}" if len(g_token_str) > 10 else "VALID_TOKEN"
else:
    GITHUB_TOKEN = "XXXX"
    masked_token = "NOT_FOUND_IN_SECRETS"

DB_FILE = "portfolio_db.csv"
API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{DB_FILE}"

def load_permanent_database():
    if not GITHUB_TOKEN or GITHUB_TOKEN == "XXXX":
        return pd.DataFrame(columns=["Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges", "Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"])
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            content = response.json()
            df = pd.read_csv(io.BytesIO(base64.b64decode(content["content"])))
            df.columns = df.columns.str.strip()
            return df
    except Exception: pass
    return pd.DataFrame(columns=["Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges", "Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"])

def save_permanent_database(df):
    if not GITHUB_TOKEN or GITHUB_TOKEN == "XXXX": return
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    sha = None
    try:
        res = requests.get(API_URL, headers=headers, timeout=10)
        if res.status_code == 200: sha = res.json()["sha"]
    except Exception: pass
    
    csv_string = df.to_csv(index=False)
    payload = {
        "message": f"🤖 Portfolio Core System Auto Sync {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "content": base64.b64encode(csv_string.encode("utf-8")).decode("utf-8")
    }
    if sha: payload["sha"] = sha
    try: requests.put(API_URL, headers=headers, json=payload, timeout=15)
    except Exception: pass

if "portfolio_data_store" not in st.session_state:
    st.session_state.portfolio_data_store = load_permanent_database()

master_df = st.session_state.portfolio_data_store

# ব্যাকঅ্যান্ড স্ট্রাকচার সেফগার্ড ভ্যালিডেশন
for required_col in ["Buy Price", "Quantity", "Buy Charges", "Sell Price", "Sell Charges", "Realized P&L", "Status"]:
    if required_col not in master_df.columns:
        master_df[required_col] = 0.0 if "Charges" in required_col or "Price" in required_col or "P&L" in required_col else ("ACTIVE" if required_col == "Status" else 0)

active_portfolio = master_df[master_df["Status"] == "ACTIVE"].reset_index(drop=True)
closed_portfolio = master_df[master_df["Status"] == "CLOSED"].reset_index(drop=True)

# GLITCH FIX CALLBACK FUNCTION
def clear_logs_callback():
    st.session_state.live_logs = []

# =========================================================================
# 🖥️ CORE BACKEND LIVE DIAGNOSTIC LOGS HUD
# =========================================================================
st.markdown("### 🖥️ CORE BACKEND LIVE DIAGNOSTIC LOGS")
with st.expander("📂 OPEN LIVE SYSTEM HARDWARE TERMINAL CONSOLE", expanded=True):
    col_t1, col_t2 = st.columns([4, 1])
    col_t1.write(f"**NSE Dynamic Array Streams:** `{len(SCREENER_WATCHLIST)} Tickers Locked` | **GitHub Bridge Status:** `{masked_token}`")
    col_t2.button("🧹 Clear Terminal Logs", on_click=clear_logs_callback, key="ultimate_clear_logs_btn")
        
    logs_list = st.session_state.get("live_logs", [])
    log_box_content = "\n".join(logs_list) if logs_list else "SYSTEM: Pipeline active. Buffer cleared. Awaiting hardware operations sync..."
    st.code(log_box_content, language="bash")

st.markdown("---")

# Navigation Command Control Panel
st.sidebar.markdown("### 🖥️ DATA ARCHITECTURE CONTROL")
menu_selection = st.sidebar.radio(
    "COMMAND CONTROLLER PANEL",
    [
        "📊 PORTFOLIO ANALYTICS",
        "🔍 LIVE SCREENER CORE",
        "🚀 MONSTER MOAT HUNT (1000%)",
        "📥 TRANSACTION EXECUTION UNIT",
        "📋 RUNNING POSITION REPLICA",
        "📡 SYSTEM HARDWARE SYNC"
    ],
    key="navigation_sidebar_radio"
)

# 🎯 SCREENER OUTPUT COLUMNS DEFINITION
ALL_METRICS_COLS = [
    "Stock", "Chart Setup", "CMP (₹)", "P/E Ratio", "ROE (%)", 
    "Sales Growth (%)", "Gross Margin (%)", "Inventory Speed (x)", 
    "Promoter (%)", "Institutions (%)", "Max DD (%)", "EMA200 Dist (%)"
]

# 🎯 100% BULLETPROOF SCREENER FILTER ENGINE (THE ABSOLUTE QUANT FIX)
def execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, min_promoter, min_ema200, additional_moat_filter=False, min_gross_margin=0.0, min_inventory_speed=0.0):
    add_log("Searching database index array...", "INFO")
    raw_df = load_offline_market_data(GITHUB_USER, GITHUB_REPO, GITHUB_TOKEN)
    
    if raw_df.empty:
        add_log("Scan Failed: Missing market_data.csv on GitHub root.", "ERROR")
        st.error("⚠️ Local data index is vacant. Execute sync loop in 'SYSTEM HARDWARE SYNC' first.")
        return
        
    try:
        # Secure strict numeric conversion to prevent formatting/filtering bypass bugs
        numeric_cols = ["Sales Growth (%)", "ROE (%)", "Market Cap (Cr)", "Promoter (%)", "EMA200 Dist (%)", "P/E Ratio", "Gross Margin (%)", "Inventory Speed (x)", "CMP (₹)"]
        for col in numeric_cols:
            if col in raw_df.columns:
                raw_df[col] = pd.to_numeric(raw_df[col], errors='coerce').fillna(0.0)
                
        # Base Quantum Rules Filtering
        q_df = raw_df[
            (raw_df["Sales Growth (%)"] >= float(min_sales)) & 
            (raw_df["ROE (%)"] >= float(min_roe)) & 
            (raw_df["Market Cap (Cr)"] >= float(min_mcap)) & 
            (raw_df["Promoter (%)"] >= float(min_promoter)) & 
            (raw_df["EMA200 Dist (%)"] >= float(min_ema200))
        ]
        
        # Upper P/E Valuation Limit logic
        if float(max_pe) > 0:
            q_df = q_df[q_df["P/E Ratio"] <= float(max_pe)]
            
        # Advanced Moat Hunter parameters integration
        if additional_moat_filter:
            q_df = q_df[
                (q_df["Gross Margin (%)"] >= float(min_gross_margin)) &
                (q_df["Inventory Speed (x)"] >= float(min_inventory_speed))
            ]
            
        if not q_df.empty:
            add_log(f"Isolated {len(q_df)} matching configurations out of the active asset universe.", "SUCCESS")
            st.success(f"🎯 Query Processed. Isolated {len(q_df)} High-Probability Target Assets.")
            
            # Formulate and render safe matching layout columns
            render_cols = [c for c in ALL_METRICS_COLS if c in q_df.columns]
            st.dataframe(q_df[render_cols].reset_index(drop=True), use_container_width=True)
        else:
            add_log("Filter layer closed. Zero matching assets located.", "WARNING")
            st.warning("No stocks match the specified quantitative parameters.")
    except Exception as e: 
        add_log(f"Screener engine execution structural fault: {str(e)}", "ERROR")
        st.error(f"Engine Exception: {str(e)}")

# =========================================================================
# MODULE 1: 📊 PORTFOLIO ANALYTICS
# =========================================================================
if menu_selection == "📊 PORTFOLIO ANALYTICS":
    st.markdown("### 📈 PREMIUM PORTFOLIO EXECUTIVE HUD OVERVIEW")
    
    if active_portfolio.empty:
        st.info("💡 Your active portfolio tracking array is vacant. Enter trades via 'TRANSACTION EXECUTION UNIT'.")
    else:
        with st.spinner("Syncing data loops with exchange ticker streams..."):
            tickers_list = [f"{str(s).strip()}.NS" for s in active_portfolio["Stock"].unique() if s]
            try:
                live_data = yf.download(tickers=tickers_list, period="1d", interval="1m", progress=False, timeout=12)
                last_prices = {}
                for s in active_portfolio["Stock"].unique():
                    tick = f"{str(s).strip()}.NS"
                    if len(tickers_list) > 1:
                        last_prices[s] = float(live_data["Close"][tick].dropna().iloc[-1])
                    else:
                        last_prices[s] = float(live_data["Close"].dropna().iloc[-1])
            except Exception:
                last_prices = {s: float(active_portfolio[active_portfolio["Stock"] == s]["Buy Price"].iloc[0]) for s in active_portfolio["Stock"].unique()}

        active_portfolio["CMP (₹)"] = active_portfolio["Stock"].map(last_prices).fillna(active_portfolio["Buy Price"])
        active_portfolio["Total Invested"] = active_portfolio["Quantity"].astype(int) * active_portfolio["Buy Price"].astype(float)
        active_portfolio["Current Value"] = active_portfolio["Quantity"].astype(int) * active_portfolio["CMP (₹)"].astype(float)
        active_portfolio["Unrealized P&L"] = active_portfolio["Current Value"] - active_portfolio["Total Invested"]
        
        tot_inv = active_portfolio["Total Invested"].sum()
        tot_cur = active_portfolio["Current Value"].sum()
        net_unr = tot_cur - tot_inv
        roi_pct = (net_unr / tot_inv * 100) if tot_inv > 0 else 0.0

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="quant-card"><div style="font-size:11px;color:#00bfff;">CURRENT EQUITY VALUE</div><div class="quant-val">₹ {tot_cur:,.2f}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="quant-card"><div style="font-size:11px;color:#a1a1aa;">CAPITAL INVESTED</div><div class="quant-val">₹ {tot_inv:,.2f}</div></div>', unsafe_allow_html=True)
        
        pnl_color = "#00ffaa" if net_unr >= 0 else "#ff3366"
        c3.markdown(f'<div class="quant-card" style="border-top:3px solid {pnl_color};"><div style="font-size:11px;color:{pnl_color};">NET UNREALIZED VARIANCE</div><div class="quant-val" style="color:{pnl_color};">₹ {net_unr:,.2f}</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="quant-card" style="border-top:3px solid {pnl_color};"><div style="font-size:11px;color:{pnl_color};">TOTAL ROI (%)</div><div class="quant-val" style="color:{pnl_color};">{roi_pct:+.2f}%</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### 🎯 Capital Asset Allocation Mix")
            fig_pie = px.pie(active_portfolio, names="Stock", values="Current Value", hole=0.4, color_discrete_sequence=px.colors.sequential.Mint_r)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e2e8f0", showlegend=True, margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with chart_col2:
            st.markdown("#### 📈 Portfolio Performance Distribution (P&L)")
            fig_bar = px.bar(active_portfolio, x="Stock", y="Unrealized P&L", color="Unrealized P&L", color_continuous_scale=["#ff3366", "#00ffaa"])
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e2e8f0", margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 📋 LIVE ASSET INVENTORY EXPANSION SLOTS")
        st.dataframe(active_portfolio[["Stock", "Quantity", "Buy Price", "CMP (₹)", "Total Invested", "Current Value", "Unrealized P&L"]], use_container_width=True)

# =========================================================================
# MODULE 2: 🔍 LIVE SCREENER CORE (FIXED)
# =========================================================================
elif menu_selection == "🔍 LIVE SCREENER CORE":
    st.subheader("🦅 CORE BATCH QUANT MATRIX SCREENER")
    c1, c2 = st.columns(2)
    min_sales = c1.number_input("Minimum Revenue Growth (%)", value=15.0, step=1.0)
    min_roe = c2.number_input("Minimum Return On Equity (%)", value=15.0, step=1.0)
    c3, c4 = st.columns(2)
    max_pe = c3.number_input("Maximum P/E Ratio Limit (0 for No Limit)", value=40.0, step=1.0)
    min_mcap = c4.number_input("Minimum Market Cap (Cr)", value=1000.0, step=500.0)
    c5, c6 = st.columns(2)
    min_promoter = c5.number_input("Minimum Promoter Ownership (%)", value=40.0, step=5.0)
    min_ema200_dist = c6.number_input("Minimum Cushion distance from 200 EMA (%)", value=1.0, step=0.5)
    
    if st.button("EXECUTE SCALPER BATCH DATA CORE SCAN"):
        execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, min_promoter, min_ema200_dist)

# =========================================================================
# MODULE 3: 🚀 MONSTER MOAT HUNT (FIXED)
# =========================================================================
elif menu_selection == "🚀 MONSTER MOAT HUNT (1000%)":
    st.subheader("🔥 HYPER-MONOPOLY MONSTER MOAT MULTIBAGGER SCALPER")
    c1, c2 = st.columns(2)
    min_sales = c1.number_input("Super-Normal Revenue Threshold Growth (%)", value=25.0, step=1.0)
    min_roe = c2.number_input("High-Monopoly Operating Target ROE (%)", value=25.0, step=1.0)
    c3, c4 = st.columns(2)
    min_gross_margin = c3.number_input("Pricing Premium Power (Minimum Gross Margin %)", value=45.0, step=5.0)
    min_inventory_speed = c4.number_input("Consumer Velocity Force (Minimum Inventory Speed x)", value=6.0, step=1.0)
    c5, c6 = st.columns(2)
    max_pe = c5.number_input("Maximum Multiples Cap (0 for No Limit)", value=35.0, step=1.0)
    min_mcap = c6.number_input("Minimum Threshold Market Cap (Cr)", value=1000.0, step=500.0)
    
    if st.button("LAUNCH MONSTER SCAN OVER 5000+ SECURITIES"):
        execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, 45.0, 2.5, additional_moat_filter=True, min_gross_margin=min_gross_margin, min_inventory_speed=min_inventory_speed)

# =========================================================================
# MODULE 4: 📥 TRANSACTION EXECUTION UNIT
# =========================================================================
elif menu_selection == "📥 TRANSACTION EXECUTION UNIT":
    st.markdown("### 📥 EXECUTIVE ORDER TRANSITS DESK")
    trade_type = st.radio("Execution Vector:", ["🛒 ACCUMULATE (BUY)", "💰 LIQUIDATE (SELL)"], horizontal=True)
    
    with st.form("trade_form", clear_on_submit=True):
        dropdown_options = sorted(list(SCREENER_WATCHLIST)) if SCREENER_WATCHLIST else ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]
        if "LIQUIDATE" in trade_type and not active_portfolio.empty:
            dropdown_options = sorted(list(active_portfolio["Stock"].unique()))
            
        stock_name = st.selectbox("Select Stock Symbol (Type to Search)", options=dropdown_options, index=None)
        input_price = st.number_input("Execution Price (INR)", min_value=0.01)
        input_qty = st.number_input("Volume Quantity (Qty)", min_value=1)
        trade_date = st.date_input("Ledger Date Seal", datetime.now())
        
        if st.form_submit_button("ROUTE ORDER TO DATA SYSTEM") and stock_name:
            master_df = load_permanent_database()
            add_log(f"Routing transaction payload: {trade_type} {input_qty} items of {stock_name}", "INFO")
            
            if "ACCUMULATE" in trade_type:
                b_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=True)
                if stock_name in master_df[master_df["Status"] == "ACTIVE"]["Stock"].values:
                    idx = master_df[(master_df["Status"] == "ACTIVE") & (master_df["Stock"] == stock_name)].index[0]
                    old_qty = int(master_df.loc[idx, "Quantity"])
                    new_qty = old_qty + input_qty
                    master_df.loc[idx, ["Buy Price", "Quantity", "Buy Charges", "Buy Date"]] = [round(((float(master_df.loc[idx, "Buy Price"]) * old_qty) + (input_price * input_qty)) / new_qty, 2), new_qty, float(master_df.loc[idx, "Buy Charges"]) + b_charges, str(trade_date)]
                else:
                    new_row = pd.DataFrame([{"Stock": stock_name, "Buy Price": round(input_price, 2), "Quantity": int(input_qty), "Buy Date": str(trade_date), "Buy Charges": b_charges, "Sell Price": 0.0, "Sell Date": "-", "Sell Charges": 0.0, "Realized P&L": 0.0, "Status": "ACTIVE"}])
                    master_df = pd.concat([master_df, new_row], ignore_index=True)
            else:
                if stock_name in master_df[master_df["Status"] == "ACTIVE"]["Stock"].values:
                    idx = master_df[(master_df["Status"] == "ACTIVE") & (master_df["Stock"] == stock_name)].index[0]
                    old_qty = int(master_df.loc[idx, "Quantity"])
                    buy_p = float(master_df.loc[idx, "Buy Price"])
                    s_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=False)
                    allocated_b_charge = float(master_df.loc[idx, "Buy Charges"]) * (input_qty / old_qty)
                    realized_pnl = round(((input_price - buy_p) * input_qty) - (allocated_b_charge + s_charges), 2)
                    
                    if input_qty >= old_qty:
                        master_df.loc[idx, ["Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"]] = [input_price, str(trade_date), s_charges, realized_pnl, "CLOSED"]
                    else:
                        master_df.loc[idx, "Quantity"] = old_qty - input_qty
                        master_df.loc[idx, "Buy Charges"] = float(master_df.loc[idx, "Buy Charges"]) - allocated_b_charge
                        closed_row = pd.DataFrame([{"Stock": stock_name, "Buy Price": buy_p, "Quantity": input_qty, "Buy Date": master_df.loc[idx, "Buy Date"], "Buy Charges": round(allocated_b_charge, 2), "Sell Price": input_price, "Sell Date": str(trade_date), "Sell Charges": s_charges, "Realized P&L": realized_pnl, "Status": "CLOSED"}])
                        master_df = pd.concat([master_df, closed_row], ignore_index=True)
                else:
                    st.error("No active exposure located for this ticker symbol.")
                    
            save_permanent_database(master_df)
            st.session_state.portfolio_data_store = master_df
            st.success(f"🔥 Transaction successfully completed for {stock_name}!")
            st.rerun()

elif menu_selection == "📋 RUNNING POSITION REPLICA":
    st.markdown("### 📋 ACTIVE RUNNING POSITION INVENTORY")
    if not active_portfolio.empty: 
        st.dataframe(active_portfolio[["Stock", "Quantity", "Buy Price", "Buy Charges", "Buy Date"]], use_container_width=True)
    else: 
        st.info("Active exposure matrix vacant.")

elif menu_selection == "📡 SYSTEM HARDWARE SYNC":
    st.subheader("🛰️ DYNAMIC EXCHANGES ARCHIVE REPLICATOR")
    if st.button("⚡ EXECUTE BATCH BULK DATA REPLICATION (CSV SYNC)"):
        with st.spinner("Compiling listed markets maps directly to GitHub..."):
            total_synced = run_offline_sync_pipeline(SCREENER_WATCHLIST, GITHUB_USER, GITHUB_REPO, GITHUB_TOKEN)
            if total_synced > 0: 
                st.success(f"🔥 SUCCESS! Generated and synced {total_synced} items to GitHub database!")
                st.rerun()

render_operational_guidelines()
render_terminal_footer()
