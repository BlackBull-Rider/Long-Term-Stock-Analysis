# app.py
import streamlit as st
import pandas as pd
import requests
import base64
import io
from datetime import datetime

# 🎯 CRITICAL BUG FIX: অ্যাপ রান হওয়ার সাথে সাথে সবার আগে সেশন স্টেট ইনিশিয়ালাইজ করা হলো
if "live_logs" not in st.session_state:
    st.session_state.live_logs = []

from stocks import SCREENER_WATCHLIST
from core.styles import apply_terminal_theme, render_branding_header, render_operational_guidelines, render_terminal_footer
from core.engine import (
    calculate_indian_market_charges, run_offline_sync_pipeline, 
    load_offline_market_data, add_log
)

# Apply UI Layout Rules safely
apply_terminal_theme()
render_branding_header()

# =========================================================================
# GITHUB DATA LAYER CONFIGURATION
# =========================================================================
GITHUB_USER = "BlackBull-Rider"  
GITHUB_REPO = "Long-Term-Stock-Analysis"  

if "MY_GITHUB_TOKEN" in st.secrets:
    GITHUB_TOKEN = st.secrets["MY_GITHUB_TOKEN"]
    # সিকিউর মাস্কিং
    g_token_str = str(GITHUB_TOKEN).strip()
    masked_token = f"{g_token_str[:6]}...{g_token_str[-4:]}" if len(g_token_str) > 10 else "VALID_TOKEN"
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

if "Status" not in master_df.columns:
    master_df["Status"] = "ACTIVE"

active_portfolio = master_df[master_df["Status"] == "ACTIVE"].reset_index(drop=True)

# =========================================================================
# 🖥️ LIVE DEBUG CONSOLE HUD (SAFEGUARD IMPLEMENTED)
# =========================================================================
st.markdown("### 🖥️ CORE BACKEND LIVE DIAGNOSTIC LOGS")
with st.expander("📂 OPEN LIVE SYSTEM HARDWARE TERMINAL CONSOLE", expanded=True):
    col_t1, col_t2 = st.columns([4, 1])
    col_t1.write(f"**NSE Dynamic Watchlist Active Array:** `{len(SCREENER_WATCHLIST)} Tickers Locked` | **API Token:** `{masked_token}`")
    if col_t2.button("🧹 Clear Terminal Logs"):
        st.session_state.live_logs = []
        st.rerun()
        
    # সেফ গার্ড গ্যারান্টি চেক
    logs_list = st.session_state.get("live_logs", [])
    log_box_content = "\n".join(logs_list) if logs_list else "SYSTEM: Pipeline active. Awaiting hardware operations sync..."
    st.code(log_box_content, language="bash")

st.markdown("---")

# Sidebar
st.sidebar.markdown("### 🖥️ DATA ARCHITECTURE CONTROL")
menu_selection = st.sidebar.radio(
    "COMMAND CONTROLLER PANEL",
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
    add_log("Initiating scan execution over synchronized market database csv...", "INFO")
    raw_df = load_offline_market_data(GITHUB_USER, GITHUB_REPO, GITHUB_TOKEN)
    if raw_df.empty:
        add_log("Scan Blocked: Remote file market_data.csv is absent or vacant.", "ERROR")
        st.error("⚠️ Local data index is empty. Navigate to 'SYSTEM HARDWARE SYNC' block and run sync pipeline first.")
        return
        
    try:
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
            add_log(f"Filter process completed successfully! Isolated {len(q_df)} active profiles.", "SUCCESS")
            st.dataframe(q_df[ALL_METRICS_COLS], use_container_width=True)
        else:
            add_log("Query execution finished. Zero matching assets indexed.", "WARNING")
            st.warning("No stocks match the given parameters.")
    except Exception as e:
        add_log(f"Query structural computation error: {str(e)}", "ERROR")

if menu_selection == "📊 PORTFOLIO ANALYTICS":
    st.markdown("### 📈 PREMIUM PORTFOLIO EXECUTIVE HUD OVERVIEW")
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
    min_ema200_dist = c6.number_input("Minimum Space distance from 200 EMA (%)", value=1.0)
    
    if st.button("EXECUTE SCALPER BATCH DATA CORE SCAN"):
        execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, min_promoter, min_ema200_dist)

elif menu_selection == "🚀 MONSTER MOAT HUNT (1000%)":
    st.subheader("🔥 HIGH-ALPHA VECTOR MONSTER MOAT RADAR")
    c1, c2 = st.columns(2)
    min_sales = c1.number_input("Super-Normal Revenue Threshold Growth (%)", value=25.0)
    min_roe = c2.number_input("High-Monopoly Target ROE (%)", value=25.0)
    if st.button("EXECUTE VECTOR ALGORITHM OVER SYNCED STOCKS"):
        execute_quant_filter_engine(min_sales, min_roe, 35.0, 1000.0, 45.0, 2.5)

elif menu_selection == "📡 SYSTEM HARDWARE SYNC":
    st.subheader("🛰️ DYNAMIC EXCHANGES ARCHIVE REPLICATOR")
    st.info(f"💡 এই বাটনে ক্লিক করলেই তোমার stocks.py ফাইলের স্ক্র্যাপার দিয়ে অটোমেটিক্যালি এনএসই থেকে ফেচ হওয়া মোট {len(SCREENER_WATCHLIST)} টি লাইভ স্টকের রリアル-টাইম ডাটা ডাউনলোড হয়ে গিটহাব রেপোতে রাইট হয়ে যাবে।")
    if st.button("⚡ EXECUTE BATCH BULK DATA REPLICATION (CSV SYNC)"):
        with st.spinner("Compiling and syncing listed markets directly to GitHub..."):
            total_synced = run_offline_sync_pipeline(SCREENER_WATCHLIST, GITHUB_USER, GITHUB_REPO, GITHUB_TOKEN)
            if total_synced > 0: 
                st.success(f"🔥 SUCCESS! Generated and synced {total_synced} items to GitHub root database!")
                st.rerun()

elif menu_selection == "📥 TRANSACTION EXECUTION UNIT":
    st.markdown("### 📥 EXECUTIVE ORDER TRANSITS DESK")
    with st.form("trade_form", clear_on_submit=True):
        # 🎯 SUGGESTION DROPDOWN FIX: SCREENER_WATCHLIST-কে ডাইরেক্ট লিস্ট হিসেবে ড্রপডাউনে লক করা হলো
        stock_name = st.selectbox(
            "Select Stock Symbol (Type to Search)", 
            options=sorted(list(SCREENER_WATCHLIST)) if SCREENER_WATCHLIST else ["RELIANCE", "TCS", "INFY", "HDFCBANK"], 
            index=None
        )
        input_price = st.number_input("Execution Price (INR)", min_value=0.01)
        input_qty = st.number_input("Volume Quantity (Qty)", min_value=1)
        
        if st.form_submit_button("ROUTE ORDER TO GITHUB DATA SYSTEM") and stock_name:
            master_df = load_permanent_database()
            b_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=True)
            new_row = pd.DataFrame([{"Stock": stock_name, "Buy Price": round(input_price, 2), "Quantity": int(input_qty), "Buy Date": datetime.now().strftime('%Y-%m-%d'), "Buy Charges": b_charges, "Status": "ACTIVE"}])
            master_df = pd.concat([master_df, new_row], ignore_index=True)
            save_permanent_database(master_df)
            st.session_state.portfolio_data_store = master_df
            st.success(f"🔥 Position lock routed successfully for {stock_name}!")
            st.rerun()


render_operational_guidelines()
render_terminal_footer()
