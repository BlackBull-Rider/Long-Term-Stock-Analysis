# app.py
import streamlit as st
import pandas as pd
import requests
import base64
import io
from datetime import datetime

from stocks import SCREENER_WATCHLIST
from core.styles import apply_terminal_theme, render_branding_header, render_operational_guidelines, render_terminal_footer
from core.engine import (
    calculate_indian_market_charges, run_offline_sync_pipeline, 
    load_offline_market_data, add_log
)

# Apply UI Layout Rules
apply_terminal_theme()
render_branding_header()

# =========================================================================
# GITHUB DATA LAYER CONFIGURATION
# =========================================================================
GITHUB_USER = "BlackBull-Rider"  
GITHUB_REPO = "Long-Term-Stock-Analysis"  

if "MY_GITHUB_TOKEN" in st.secrets:
    GITHUB_TOKEN = st.secrets["MY_GITHUB_TOKEN"]
    masked_token = f"{GITHUB_TOKEN[:6]}...{GITHUB_TOKEN[-4:]}" if len(GITHUB_TOKEN) > 10 else "VALID_TOKEN"
else:
    GITHUB_TOKEN = "XXXX"
    masked_token = "NOT_FOUND_IN_SECRETS"

DB_FILE = "portfolio_db.csv"
API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{DB_FILE}"

def load_permanent_database():
    if not GITHUB_TOKEN or GITHUB_TOKEN == "XXXX":
        return pd.DataFrame(columns=["Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges", "Status"])
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            content = response.json()
            df = pd.read_csv(io.BytesIO(base64.b64decode(content["content"])))
            df.columns = df.columns.str.strip()
            return df
    except Exception: pass
    return pd.DataFrame(columns=["Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges", "Status"])

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
        "message": f"🤖 Portfolio Sync {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "content": base64.b64encode(csv_string.encode("utf-8")).decode("utf-8")
    }
    if sha: payload["sha"] = sha
    try: requests.put(API_URL, headers=headers, json=payload, timeout=15)
    except Exception: pass

if "portfolio_data_store" not in st.session_state:
    st.session_state.portfolio_data_store = load_permanent_database()

master_df = st.session_state.portfolio_data_store

# Ensure 'Status' column exists to prevent column key crashes
if "Status" not in master_df.columns:
    master_df["Status"] = "ACTIVE"

active_portfolio = master_df[master_df["Status"] == "ACTIVE"].reset_index(drop=True)

# =========================================================================
# LIVE TERMINAL CONSOLE 
# =========================================================================
st.markdown("### 🖥️ CORE BACKEND LIVE DIAGNOSTIC LOGS")
with st.expander("📂 OPEN LIVE SYSTEM HARDWARE TERMINAL CONSOLE", expanded=True):
    col_t1, col_t2 = st.columns([4, 1])
    col_t1.write(f"**NSE Universe Stream:** `{len(SCREENER_WATCHLIST)} Assets Indexed` | **Token Status:** `{masked_token}`")
    if col_t2.button("🧹 Clear Terminal Logs"):
        st.session_state.live_logs = []
        st.rerun()
        
    log_box_content = "\n".join(st.session_state.live_logs) if st.session_state.live_logs else "SYSTEM: Ready for heavy calculations layers..."
    st.code(log_box_content, language="bash")

st.markdown("---")

# App Sidebar Navigator
st.sidebar.markdown("### 🖥️ COMMAND CENTRE")
menu_selection = st.sidebar.radio(
    "SELECT MODULE",
    [
        "📊 PORTFOLIO ANALYTICS",
        "🔍 LIVE SCREENER CORE",
        "🚀 MONSTER MOAT HUNT (1000%)",
        "📥 TRANSACTION EXECUTION UNIT",
        "📡 SYSTEM HARDWARE SYNC"
    ]
)

ALL_METRICS_COLS = [
    "Stock", "Chart Setup", "CMP (₹)", "P/E Ratio", "ROE (%)", 
    "Sales Growth (%)", "Gross Margin (%)", "Inventory Speed (x)", 
    "Promoter (%)", "Institutions (%)", "Max DD (%)", "EMA200 Dist (%)"
]

def execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, min_promoter, min_ema200):
    add_log("Searching synchronized market database csv...", "INFO")
    raw_df = load_offline_market_data(GITHUB_USER, GITHUB_REPO, GITHUB_TOKEN)
    
    if raw_df.empty:
        add_log("Scan Failed: market_data.csv is absent or empty on GitHub repository.", "ERROR")
        st.error("⚠️ Local market cache is blank. Please go to 'SYSTEM HARDWARE SYNC' and execute data replication.")
        return
        
    try:
        # Secure type alignment to prevent filtering errors
        for col in ["Sales Growth (%)", "ROE (%)", "Market Cap (Cr)", "Promoter (%)", "EMA200 Dist (%)", "P/E Ratio"]:
            if col in raw_df.columns:
                raw_df[col] = pd.to_numeric(raw_df[col], errors='coerce').fillna(0.0)
                
        q_df = raw_df[
            (raw_df["Sales Growth (%)"] >= float(min_sales)) & 
            (raw_df["ROE (%)"] >= float(min_roe)) & 
            (raw_df["Market Cap (Cr)"] >= float(min_mcap)) & 
            (raw_df["Promoter (%)"] >= float(min_promoter)) & 
            (raw_df["EMA200 Dist (%)"] >= float(min_ema200))
        ]
        
        if max_pe > 0:
            q_df = q_df[q_df["P/E Ratio"] <= float(max_pe)]
            
        if not q_df.empty:
            add_log(f"Success! Found {len(q_df)} alpha configurations.", "SUCCESS")
            # Filter only safe rendering columns
            render_cols = [c for c in ALL_METRICS_COLS if c in q_df.columns]
            st.dataframe(q_df[render_cols], use_container_width=True)
        else:
            add_log("Filter finished. Zero matching assets indexed.", "WARNING")
            st.warning("No stocks match the given parameters.")
    except Exception as e:
        add_log(f"Query Exception Error: {str(e)}", "ERROR")

if menu_selection == "📊 PORTFOLIO ANALYTICS":
    st.markdown("### 📈 PORTFOLIO HUD EXECUTIVE DATA")
    if active_portfolio.empty:
        st.info("💡 Portfolio ledger is empty. Enter active slots via Order Desk.")
    else:
        st.dataframe(active_portfolio, use_container_width=True)

elif menu_selection == "🔍 LIVE SCREENER CORE":
    st.subheader("🦅 DYNAMIC EXCHANGE UNIVERSE MATRIX")
    c1, c2 = st.columns(2)
    min_sales = c1.number_input("Minimum Revenue Growth (%)", value=15.0)
    min_roe = c2.number_input("Minimum Return On Equity (%)", value=15.0)
    c3, c4 = st.columns(2)
    max_pe = c3.number_input("Maximum P/E Ratio (0 for No Limit)", value=40.0)
    min_mcap = c4.number_input("Minimum Market Cap (Cr)", value=500.0)
    c5, c6 = st.columns(2)
    min_promoter = c5.number_input("Minimum Promoter Ownership (%)", value=40.0)
    min_ema200_dist = c6.number_input("Minimum distance from 200 EMA (%)", value=1.0)
    
    if st.button("RUN SCALPER BATCH DATA CORE SCAN"):
        execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, min_promoter, min_ema200_dist)

elif menu_selection == "🚀 MONSTER MOAT HUNT (1000%)":
    st.subheader("🔥 HIGH-ALPHA VECTOR MONSTER MOAT RADAR")
    c1, c2 = st.columns(2)
    min_sales = c1.number_input("Super-Normal Revenue Threshold Growth (%)", value=25.0)
    min_roe = c2.number_input("High-Monopoly Target ROE (%)", value=25.0)
    if st.button("LAUNCH MONSTER SCAN OVER 5000+ SECURITIES"):
        execute_quant_filter_engine(min_sales, min_roe, 35.0, 1000.0, 45.0, 2.5)

elif menu_selection == "📡 SYSTEM HARDWARE SYNC":
    st.subheader("🛰️ DYNAMIC EXCHANGES ARCHIVE REPLICATOR")
    st.warning("⚡ সাবধান: এটি রান করলে প্যারালাল থ্রেডে এনএসই থেকে রিয়েল-টাইম ডেটা গিটহাবে ডাউনলোড হবে। সম্পূর্ণ কমপ্লিট হতে ডেটার সাইজ অনুযায়ী কিছুটা সময় লাগতে পারে।")
    if st.button("⚡ EXECUTE BATCH BULK DATA REPLICATION (CSV SYNC)"):
        with st.spinner("Compiling and syncing listed markets directly to GitHub..."):
            total_synced = run_offline_sync_pipeline(SCREENER_WATCHLIST, GITHUB_USER, GITHUB_REPO, GITHUB_TOKEN)
            if total_synced > 0: 
                st.success(f"🔥 BOOM! Synchronized {total_synced} items to GitHub root database file!")
                st.rerun()

elif menu_selection == "📥 TRANSACTION EXECUTION UNIT":
    st.markdown("### 📥 EXECUTIVE ORDER TRANSIT DESK")
    with st.form("trade_form", clear_on_submit=True):
        stock_name = st.text_input("Enter NSE Stock Symbol").upper().strip()
        input_price = st.number_input("Execution Price (INR)", min_value=0.01)
        input_qty = st.number_input("Volume Quantity (Qty)", min_value=1)
        if st.form_submit_button("ROUTE ORDER TO DATA SYSTEM") and stock_name:
            master_df = load_permanent_database()
            b_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=True)
            new_row = pd.DataFrame([{"Stock": stock_name, "Buy Price": round(input_price, 2), "Quantity": int(input_qty), "Buy Date": datetime.now().strftime('%Y-%m-%d'), "Buy Charges": b_charges, "Status": "ACTIVE"}])
            master_df = pd.concat([master_df, new_row], ignore_index=True)
            save_permanent_database(master_df)
            st.session_state.portfolio_data_store = master_df
            st.success(f"Position lock routed successfully for {stock_name}!")
            st.rerun()

render_operational_guidelines()
render_terminal_footer()
