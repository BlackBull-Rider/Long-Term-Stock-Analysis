# app.py
import streamlit as st
import pandas as pd
import requests
import base64
import io
from datetime import datetime
import yfinance as yf
import plotly.express as px

if "live_logs" not in st.session_state:
    st.session_state.live_logs = []

from stocks import SCREENER_WATCHLIST
from core.styles import apply_terminal_theme, render_branding_header, render_operational_guidelines, render_terminal_footer
from core.engine import calculate_indian_market_charges, run_offline_sync_pipeline, add_log

apply_terminal_theme()
render_branding_header()

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

# 🎯 র‍্যাম ক্যাশ মেকানিজম (ইনপুট টাইপিং গ্লিচ পুরোপুরি বন্ধ করার জন্য)
@st.cache_data(ttl=300, show_spinner=False)
def load_cached_market_data(user, repo, token):
    git_api_url = f"https://api.github.com/repos/{user}/{repo}/contents/market_data.csv"
    headers = {"Authorization": f"token {str(token).strip()}"}
    try:
        response = requests.get(git_api_url, headers=headers, timeout=12)
        if response.status_code == 200:
            content = response.json()
            csv_bytes = base64.b64decode(content["content"])
            return pd.read_csv(io.BytesIO(csv_bytes))
    except Exception: pass
    return pd.DataFrame()

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

for required_col in ["Buy Price", "Quantity", "Buy Charges", "Sell Price", "Sell Charges", "Realized P&L", "Status"]:
    if required_col not in master_df.columns:
        master_df[required_col] = 0.0 if "Charges" in required_col or "Price" in required_col or "P&L" in required_col else ("ACTIVE" if required_col == "Status" else 0)

active_portfolio = master_df[master_df["Status"] == "ACTIVE"].reset_index(drop=True)

def clear_logs_callback():
    st.session_state.live_logs = []

# =========================================================================
# 🖥️ CORE BACKEND TERMINAL LOGS HUD
# =========================================================================
st.markdown("### 🖥️ CORE BACKEND LIVE DIAGNOSTIC LOGS")
with st.expander("📂 OPEN LIVE SYSTEM HARDWARE TERMINAL CONSOLE", expanded=True):
    col_t1, col_t2 = st.columns([4, 1])
    col_t1.write(f"**NSE Dynamic Array Streams:** `{len(SCREENER_WATCHLIST)} Tickers Locked` | **GitHub Bridge:** `{masked_token}`")
    col_t2.button("🧹 Clear Terminal Logs", on_click=clear_logs_callback, key="ultimate_clear_logs_btn")
        
    logs_list = st.session_state.get("live_logs", [])
    log_box_content = "\n".join(logs_list) if logs_list else "SYSTEM: Data nodes responsive. Premium analytics stream active..."
    st.code(log_box_content, language="bash")

st.markdown("---")

# Navigation Controller
st.sidebar.markdown("### 🖥️ DATA ARCHITECTURE CONTROL")
menu_selection = st.sidebar.radio(
    "COMMAND CONTROLLER PANEL",
    ["📊 PORTFOLIO ANALYTICS", "🔍 LIVE SCREENER CORE", "🚀 MONSTER MOAT HUNT (1000%)", "📥 TRANSACTION EXECUTION UNIT", "📋 RUNNING POSITION REPLICA", "📡 SYSTEM HARDWARE SYNC"],
    key="navigation_sidebar_radio"
)

ALL_METRICS_COLS = [
    "Stock", "Chart Setup", "CMP (₹)", "P/E Ratio", "ROE (%)", 
    "Sales Growth (%)", "Gross Margin (%)", "Inventory Speed (x)", 
    "Marketing Efficiency (x)", "Promoter (%)", "Institutions (%)", 
    "Max DD (%)", "EMA200 Dist (%)", "Dividend (%)", "Beta"
]

# 🎯 ১৪টি কোর প্যারামিটার প্রাইস ভেলোসিটি ফিল্টার ইঞ্জিন (১০০% বাগ-ফ্রি বড় লজিক)
def execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, min_promoter, min_ema200, additional_moat_filter=False, gross_m=0.0, inv_spd=0.0, inst_val=0.0, dd_limit=-100.0, target_duration="1Y", target_return=0.0):
    raw_df = load_cached_market_data(GITHUB_USER, GITHUB_REPO, GITHUB_TOKEN)
    if raw_df.empty:
        st.error("⚠️ Local data cache is blank. Please go to 'SYSTEM HARDWARE SYNC' and click sync button first.")
        return
        
    try:
        filtered_rows = []
        dur_col = f"Return {target_duration} (%)"
        
        for idx, row in raw_df.iterrows():
            try:
                # ১. ড্রপডাউন থেকে সিলেক্ট করা বছরের রিটার্ন চেক
                actual_ret = pd.to_numeric(row.get(dur_col, 0.0), errors='coerce')
                if pd.isna(actual_ret) or actual_ret < float(target_return): continue
                
                s_growth = pd.to_numeric(row.get("Sales Growth (%)", 0.0), errors='coerce')
                if pd.isna(s_growth) or s_growth < float(min_sales): continue
                
                roe_val = pd.to_numeric(row.get("ROE (%)", 0.0), errors='coerce')
                if pd.isna(roe_val) or roe_val < float(min_roe): continue
                
                m_cap = pd.to_numeric(row.get("Market Cap (Cr)", 0.0), errors='coerce')
                if pd.isna(m_cap) or m_cap < float(min_mcap): continue
                
                prom = pd.to_numeric(row.get("Promoter (%)", 0.0), errors='coerce')
                if pd.isna(prom) or prom < float(min_promoter): continue
                
                ema_dist = pd.to_numeric(row.get("EMA200 Dist (%)", 0.0), errors='coerce')
                if pd.isna(ema_dist) or ema_dist < float(min_ema200): continue
                
                pe_val = pd.to_numeric(row.get("P/E Ratio", 0.0), errors='coerce')
                if float(max_pe) > 0 and (pd.isna(pe_val) or pe_val > float(max_pe)): continue
                    
                if additional_moat_filter:
                    g_margin = pd.to_numeric(row.get("Gross Margin (%)", 0.0), errors='coerce')
                    if pd.isna(g_margin) or g_margin < float(gross_m): continue
                    
                    i_speed = pd.to_numeric(row.get("Inventory Speed (x)", 0.0), errors='coerce')
                    if pd.isna(i_speed) or i_speed < float(inv_spd): continue
                    
                    inst = pd.to_numeric(row.get("Institutions (%)", 0.0), errors='coerce')
                    if pd.isna(inst) or inst < float(inst_val): continue
                    
                    dd = pd.to_numeric(row.get("Max DD (%)", 0.0), errors='coerce')
                    if pd.isna(dd) or dd < float(dd_limit): continue

                filtered_rows.append(row)
            except Exception: continue
                
        if filtered_rows:
            q_df = pd.DataFrame(filtered_rows)
            st.success(f"🎯 Strategy Filter Complete. Isolated {len(q_df)} High-Velocity Profiles.")
            
            # ড্রপডাউন থেকে সিলেক্ট করা বছরের রিটার্ন কলামটি আউটপুট টেবিলে ডাইনামিকালি যোগ করা হলো
            render_cols = list(ALL_METRICS_COLS)
            if dur_col not in render_cols:
                render_cols.append(dur_col)
                
            st.dataframe(q_df[render_cols].reset_index(drop=True), use_container_width=True)
        else:
            st.warning("No listed equities match the active parameters.")
    except Exception as e: st.error(f"Screener Structural Fault: {str(e)}")

# =========================================================================
# SYSTEM LAYOUT MODULES
# =========================================================================
if menu_selection == "📊 PORTFOLIO ANALYTICS":
    st.markdown("### 📈 PREMIUM PORTFOLIO EXECUTIVE HUD OVERVIEW")
    if active_portfolio.empty:
        st.info("💡 Portfolio array is empty. Route assets via Transaction Unit.")
    else:
        with st.spinner("Syncing exchange ticker streams..."):
            tickers_list = [f"{str(s).strip()}.NS" for s in active_portfolio["Stock"].unique() if s]
            try:
                live_data = yf.download(tickers=tickers_list, period="1d", interval="1m", progress=False, timeout=12)
                last_prices = {}
                for s in active_portfolio["Stock"].unique():
                    tick = f"{str(s).strip()}.NS"
                    last_prices[s] = float(live_data["Close"][tick].dropna().iloc[-1]) if len(tickers_list) > 1 else float(live_data["Close"].dropna().iloc[-1])
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
        c1.metric("CURRENT EQUITY VALUE", f"₹ {tot_cur:,.2f}")
        c2.metric("CAPITAL INVESTED", f"₹ {tot_inv:,.2f}")
        c3.metric("NET UNREALIZED GAIN", f"₹ {net_unr:,.2f}")
        c4.metric("NET ROI (%)", f"{roi_pct:+.2f}%")

        st.markdown("---")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            fig_pie = px.pie(active_portfolio, names="Stock", values="Current Value", hole=0.4, color_discrete_sequence=px.colors.sequential.Mint_r)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e2e8f0", margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_pie, use_container_width=True)
        with chart_col2:
            fig_bar = px.bar(active_portfolio, x="Stock", y="Unrealized P&L", color="Unrealized P&L", color_continuous_scale=["#ff3366", "#00ffaa"])
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e2e8f0", margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")
        st.dataframe(active_portfolio[["Stock", "Quantity", "Buy Price", "CMP (₹)", "Total Invested", "Current Value", "Unrealized P&L"]], use_container_width=True)

# 🔍 LIVE SCREENER CORE (১ বছর থেকে ৫০ বছরের বিত্তম ফিক্স)
elif menu_selection == "🔍 LIVE SCREENER CORE":
    st.subheader("🦅 CORE BATCH QUANT MATRIX (১Y - ৫০Y প্যারামিটার সচল)")
    
    # 🎯 ১ থেকে ৫০ বছরের ডাইনামিক ড্রপডাউন বিত্তম
    year_options = [f"{i}Y" for i in range(1, 51)]
    
    v1, v2 = st.columns(2)
    target_dur = v1.selectbox("Target Velocity Duration Period", options=year_options, index=0, key="core_scr_dur_final")
    min_return = v2.number_input("Minimum Expected Yield Target Return (%)", value=20.0, key="core_scr_ret_final")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    min_sales = c1.number_input("Minimum Revenue Growth (%)", value=15.0, key="cs_sales")
    min_roe = c2.number_input("Minimum Return On Equity (%)", value=15.0, key="cs_roe")
    c3, c4 = st.columns(2)
    max_pe = c3.number_input("Maximum P/E Ratio Limit (0 for No Limit)", value=40.0, key="cs_pe")
    min_mcap = c4.number_input("Minimum Market Cap (Cr)", value=1000.0, key="cs_mcap")
    c5, c6 = st.columns(2)
    min_promoter = c5.number_input("Minimum Promoter Ownership (%)", value=40.0, key="cs_prom")
    min_ema200_dist = c6.number_input("Minimum Cushion Space from 200 EMA (%)", value=1.0, key="cs_emad")
    
    # টাইপিং গ্লিচ লকড বাটন সাবমিশন
    if st.button("EXECUTE SCALPER BATCH DATA CORE SCAN", key="core_scan_trigger_btn"):
        execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, min_promoter, min_ema200_dist, target_duration=target_dur, target_return=min_return)

# 🚀 MONSTER MOAT HUNT (১ বছর থেকে ৫০ বছরের বিত্তম ফিক্স)
elif menu_selection == "🚀 MONSTER MOAT HUNT (1000%)":
    st.subheader("🔥 HYPER-MONOPOLY MONSTER MOAT RADAR (১Y - ৫০Y প্যারামিটার সচল)")
    
    year_options = [f"{i}Y" for i in range(1, 51)]
    
    v1, v2 = st.columns(2)
    target_dur = v1.selectbox("Moat Velocity Window Selection", options=year_options, index=4, key="moat_scr_dur_final") # Default 5Y
    min_return = v2.number_input("Multibagger Momentum Threshold Return (%)", value=100.0, key="moat_scr_ret_final")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    min_sales = c1.number_input("Super-Normal Revenue Threshold Growth (%)", value=25.0, key="mm_sales")
    min_roe = c2.number_input("High-Alpha Operating Target ROE (%)", value=25.0, key="mm_roe")
    c3, c4 = st.columns(2)
    min_gross_margin = c3.number_input("Pricing Premium Power (Minimum Gross Margin %)", value=45.0, key="mm_gross")
    min_inventory_speed = c4.number_input("Consumer Velocity Force (Minimum Inventory Speed x)", value=6.0, key="mm_inv")
    c5, c6 = st.columns(2)
    min_inst = c5.number_input("Minimum Institutional Allocation Layer (%)", value=15.0, key="mm_inst")
    max_dd_limit = c6.number_input("Maximum Operational Drawdown Boundary (%)", value=-45.0, key="mm_dd")
    
    col_x1, col_x2 = st.columns(2)
    max_pe = col_x1.number_input("Maximum Multiples Cap", value=35.0, key="mm_pe")
    min_mcap = col_x2.number_input("Minimum Threshold Market Cap (Cr)", value=1000.0, key="mm_mcap")
    
    if st.button("LAUNCH MONSTER SCAN OVER 5000+ SECURITIES", key="moat_scan_trigger_btn"):
        execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, 45.0, 2.5, additional_moat_filter=True, gross_m=min_gross_margin, inv_spd=min_inventory_speed, inst_val=min_inst, dd_limit=max_dd_limit, target_duration=target_dur, target_return=min_return)

elif menu_selection == "📥 TRANSACTION EXECUTION UNIT":
    st.markdown("### 📥 EXECUTIVE ORDER TRANSITS DESK")
    trade_type = st.radio("Execution Vector:", ["🛒 ACCUMULATE (BUY)", "💰 LIQUIDATE (SELL)"], horizontal=True)
    with st.form("trade_form", clear_on_submit=True):
        dropdown_options = sorted(list(SCREENER_WATCHLIST)) if SCREENER_WATCHLIST else ["RELIANCE", "TCS", "INFY", "HDFCBANK"]
        if "LIQUIDATE" in trade_type and not active_portfolio.empty:
            dropdown_options = sorted(list(active_portfolio["Stock"].unique()))
        stock_name = st.selectbox("Select Stock Symbol (Type to Search)", options=dropdown_options, index=None)
        input_price = st.number_input("Execution Price (INR)", min_value=0.01)
        input_qty = st.number_input("Volume Quantity (Qty)", min_value=1)
        if st.form_submit_button("ROUTE ORDER TO DATA SYSTEM") and stock_name:
            master_df = load_permanent_database()
            b_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=True)
            new_row = pd.DataFrame([{"Stock": stock_name, "Buy Price": round(input_price, 2), "Quantity": int(input_qty), "Buy Date": datetime.now().strftime('%Y-%m-%d'), "Buy Charges": b_charges, "Status": "ACTIVE"}])
            master_df = pd.concat([master_df, new_row], ignore_index=True)
            save_permanent_database(master_df)
            st.session_state.portfolio_data_store = master_df
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
                st.cache_data.clear()
                st.rerun()

render_operational_guidelines()
render_terminal_footer()
