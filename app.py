# app.py
import streamlit as st
import pandas as pd
import random
import yfinance as yf
import requests
import base64
import io
from datetime import datetime
import plotly.express as px

from stocks import SCREENER_WATCHLIST
from core.styles import apply_terminal_theme, render_branding_header, render_operational_guidelines, render_terminal_footer
from core.engine import (
    calculate_indian_market_charges, run_offline_sync_pipeline, 
    load_offline_market_data, scan_ipo_fresh_listings
)

# Launch HUD Frame Core
apply_terminal_theme()
render_branding_header()

# =========================================================================
# 🦅 GITHUB HARD-WRITE ENGINE ROOT CONFIG (FIXED FOR BISWAJIT)
# =========================================================================
GITHUB_USER = "BlackBull-Rider"  
GITHUB_REPO = "Long-Term-Stock-Analysis"  

if "MY_GITHUB_TOKEN" in st.secrets:
    GITHUB_TOKEN = st.secrets["MY_GITHUB_TOKEN"]
else:
    GITHUB_TOKEN = "XXXX"

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
            csv_bytes = base64.b64decode(content["content"])
            df = pd.read_csv(io.BytesIO(csv_bytes))
            df.columns = df.columns.str.strip()
            return df
    except: pass
    return pd.DataFrame(columns=["Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges", "Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"])

def save_permanent_database(df):
    if not GITHUB_TOKEN or GITHUB_TOKEN == "XXXX":
        st.error("❌ GitHub Token is Missing in Streamlit Secrets!")
        return
        
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    sha = None
    try:
        res = requests.get(API_URL, headers=headers, timeout=10)
        if res.status_code == 200: sha = res.json()["sha"]
    except: pass
    
    csv_string = df.to_csv(index=False)
    encoded_content = base64.b64encode(csv_string.encode("utf-8")).decode("utf-8")
    payload = {
        "message": f"🤖 Portfolio Auto-Sync {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "content": encoded_content
    }
    if sha: payload["sha"] = sha
    
    try:
        response = requests.put(API_URL, headers=headers, json=payload, timeout=15)
        if response.status_code in [200, 201]: 
            st.success("🎯 Portfolio Synced with GitHub Root!")
            st.toast("Portfolio Sync Completed!", icon="🦅")
        else:
            st.error(f"❌ GitHub API Error: {response.status_code}. Please check if the token has 'repo' scope.")
    except: pass

if "portfolio_data_store" not in st.session_state:
    st.session_state.portfolio_data_store = load_permanent_database()

master_df = st.session_state.portfolio_data_store
active_portfolio = master_df[master_df["Status"] == "ACTIVE"].reset_index(drop=True)
closed_portfolio = master_df[master_df["Status"] == "CLOSED"].reset_index(drop=True)

# Navigation Control Menu
st.sidebar.markdown("### 🖥️ QUANT COMMANDS")
menu_selection = st.sidebar.radio(
    "COMMAND CONTROLLER PANEL",
    [
        "📊 PORTFOLIO ANALYTICS",
        "🔍 LIVE SCREENER CORE",
        "🚀 MONSTER MOAT HUNT (1000%)",
        "🔮 FRESH IPO MONITOR",
        "📥 TRANSACTION EXECUTION UNIT",
        "📋 RUNNING POSITION REPLICA",
        "📡 SYSTEM HARDWARE SYNC"
    ]
)

ALL_METRICS_COLS = [
    "Stock", "Chart Setup", "CMP (₹)", "P/E Ratio", "ROE (%)", 
    "Sales Growth (%)", "Gross Margin (%)", "Inventory Speed (x)", 
    "Marketing Efficiency (x)", "Promoter (%)", "Institutions (%)", 
    "Max DD (%)", "EMA200 Dist (%)", "Dividend (%)", "Beta", "System Action"
]

def execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, min_promoter, min_ema200, additional_moat_filter=False, gross_m=0, inv_spd=0, inst_val=0, dd_limit=-100):
    raw_df = load_offline_market_data(GITHUB_USER, GITHUB_REPO, GITHUB_TOKEN)
    if raw_df.empty:
        st.warning("⚠️ Local stock database file is currently empty. Run the 'SYSTEM HARDWARE SYNC' compiler module first.")
        return
        
    filtered_results = []
    for _, res in raw_df.iterrows():
        try:
            if (res["Sales Growth (%)"] >= min_sales and res["ROE (%)"] >= min_roe and 
                res["Market Cap (Cr)"] >= min_mcap and (max_pe == 0 or res["P/E Ratio"] <= max_pe) and
                res["Promoter (%)"] >= min_promoter and res["EMA200 Dist (%)"] >= min_ema200):
                
                if additional_moat_filter:
                    if not (res["Gross Margin (%)"] >= gross_m and res["Inventory Speed (x)"] >= inv_spd and
                            res["Institutions (%)"] >= inst_val and res["Max DD (%)"] >= dd_limit):
                        continue
                        
                valuation_tag = "DISCOUNTED BASE" if res["P/E Ratio"] < max_pe else "PREMIUM VALUE"
                action_signal = "HOLD" if res["CMP (₹)"] > res["EMA50"] else "BOOK 50%"
                
                filtered_results.append({
                    "Stock": f"{res['Stock']} [{valuation_tag}]", "Chart Setup": res["Chart Setup"], "CMP (₹)": res["CMP (₹)"],
                    "P/E Ratio": res["P/E Ratio"], "ROE (%)": res["ROE (%)"], "Sales Growth (%)": res["Sales Growth (%)"],
                    "Gross Margin (%)": res["Gross Margin (%)"], "Inventory Speed (x)": res["Inventory Speed (x)"],
                    "Marketing Efficiency (x)": res["Marketing Efficiency (x)"], "Promoter (%)": res["Promoter (%)"],
                    "Institutions (%)": res["Institutions (%)"], "Max DD (%)": res["Max DD (%)"], 
                    "EMA200 Dist (%)": f"{res['EMA200 Dist (%)']:.1f}%", "Dividend (%)": res["Dividend (%)"], "Beta": res["Beta"],
                    "System Action": action_signal
                })
        except: continue
        
    if filtered_results:
        df_final = pd.DataFrame(filtered_results)[ALL_METRICS_COLS]
        st.success(f"🎯 Query Processed. Isolated {len(df_final)} assets.")
        st.dataframe(df_final, use_container_width=True)
    else:
        st.warning("No matches located under current parameters.")

# Routing Logic Blocks
if menu_selection == "📊 PORTFOLIO ANALYTICS":
    st.markdown("### 📈 PREMIUM PORTFOLIO EXECUTIVE HUD OVERVIEW")
    if active_portfolio.empty:
        st.info("💡 Position array is empty. Populate slots via Transaction Unit.")
    else:
        with st.spinner("Syncing data loops with exchange tickers..."):
            tickers_list = [f"{s}.NS" for s in active_portfolio["Stock"].unique()]
            try:
                live_data = yf.download(tickers=tickers_list, period="1d", interval="1m", progress=False)
                last_prices = {}
                for s in active_portfolio["Stock"].unique():
                    tick = f"{s}.NS"
                    last_prices[s] = float(live_data["Close"][tick].dropna().iloc[-1]) if len(tickers_list) > 1 else float(live_data["Close"].dropna().iloc[-1])
            except:
                last_prices = {s: float(active_portfolio[active_portfolio["Stock"] == s]["Buy Price"].iloc[0]) for s in active_portfolio["Stock"].unique()}

        active_portfolio["CMP (₹)"] = active_portfolio["Stock"].map(last_prices)
        active_portfolio["Total Invested"] = active_portfolio["Quantity"] * active_portfolio["Buy Price"]
        active_portfolio["Current Value"] = active_portfolio["Quantity"] * active_portfolio["CMP (₹)"]
        active_portfolio["Unrealized P&L"] = active_portfolio["Current Value"] - active_portfolio["Total Invested"]
        
        tot_inv = active_portfolio["Total Invested"].sum()
        tot_cur = active_portfolio["Current Value"].sum()
        net_unr = tot_cur - tot_inv
        roi_pct = (net_unr / tot_inv * 100) if tot_inv > 0 else 0.0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("CURRENT EQUITY VALUE", f"₹ {tot_cur:,.2f}")
        c2.metric("CAPITAL INVESTED", f"₹ {tot_inv:,.2f}")
        c3.metric("NET UNREALIZED P&L", f"₹ {net_unr:,.2f}", delta=f"{roi_pct:.2f}%")
        c4.metric("TOTAL ROI PERCENTAGE", f"{roi_pct:+.2f}%")

        st.markdown("---")
        st.dataframe(active_portfolio[["Stock", "Quantity", "Buy Price", "CMP (₹)", "Total Invested", "Current Value", "Unrealized P&L"]], use_container_width=True)

elif menu_selection == "🔍 LIVE SCREENER CORE":
    st.subheader("🦅 CORE BATCH QUANT MATRIX")
    col_f1, col_f2 = st.columns(2)
    min_sales = col_f1.number_input("Minimum Revenue Growth (%)", value=15.0)
    min_roe = col_f2.number_input("Minimum Return On Equity (%)", value=15.0)
    col_f3, col_f4 = st.columns(2)
    max_pe = col_f3.number_input("Maximum P/E Ratio Limit", value=40.0)
    min_mcap = col_f4.number_input("Minimum Market Cap (Cr)", value=1000.0)
    col_o1, col_o2 = st.columns(2)
    min_promoter = col_o1.number_input("Minimum Promoter Ownership (%)", value=40.0)
    min_ema200_dist = col_o2.number_input("Minimum Cushion Space from 200 EMA (%)", value=2.0)
    if st.button("EXECUTE LIVE SCREENER PARALLEL PROCESS"):
        execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, min_promoter, min_ema200_dist)

elif menu_selection == "🚀 MONSTER MOAT HUNT (1000%)":
    st.subheader("🔥 HYPER-MONOPOLY MONSTER MOAT SCANNER")
    col_m1, col_m2 = st.columns(2)
    min_gross_margin = col_m1.number_input("Pricing Premium Power (Minimum Gross Margin %)", value=45.0)
    min_inventory_speed = col_m2.number_input("Consumer Velocity Force (Minimum Inventory Speed x)", value=6.0)
    col_m3, col_m4 = st.columns(2)
    min_sales = col_m3.number_input("Minimum Sales Growth Rate (%)", value=25.0)
    min_roe = col_m4.number_input("Minimum Operational ROE (%)", value=25.0)
    col_m5, col_m6 = st.columns(2)
    max_pe = col_m5.number_input("Maximum Multiples Cap", value=35.0)
    min_mcap = col_m6.number_input("Minimum Threshold Market Cap (Cr)", value=1000.0)
    col_m7, col_m8 = st.columns(2)
    min_promoter = col_m7.number_input("Minimum Core Promoter Holding (%)", value=40.0)
    min_ema200_dist = col_m8.number_input("Minimum Cushion Space from 200 EMA (%)", value=3.0)
    col_mx1, col_mx2 = st.columns(2)
    min_inst = col_mx1.number_input("Minimum Institutional Allocation Layer (%)", value=15.0)
    max_dd_limit = col_mx2.number_input("Maximum Operational Drawdown Boundary (%)", value=-40.0)
    if st.button("RUN 1000% MULTIBAGGER INSIGHT ENGINE"):
        execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, min_promoter, min_ema200_dist, additional_moat_filter=True, gross_m=min_gross_margin, inv_spd=min_inventory_speed, inst_val=min_inst, dd_limit=max_dd_limit)

elif menu_selection == "📡 SYSTEM HARDWARE SYNC":
    st.subheader("🛰️ COLD REPOSITORY DATA SYNC PIPELINE")
    if st.button("⚡ EXECUTE BATCH BULK DATA REPLICATION (CSV SYNC)"):
        with st.spinner("Downloading and compiling exchange assets maps directly to GitHub..."):
            total_synced = run_offline_sync_pipeline(SCREENER_WATCHLIST, GITHUB_USER, GITHUB_REPO, GITHUB_TOKEN)
            if total_synced > 0: 
                st.success(f"🔥 SUCCESS! Generated and synced {total_synced} items to GitHub root repository!")
            else:
                st.error("❌ Sync Refused. Please check if your token has full 'repo' permission or if your repo name is exact.")

elif menu_selection == "🔮 FRESH IPO MONITOR":
    st.markdown("### 🔮 FRESH LISTINGS MONITOR")
    if st.button("SCAN FRESH IPO SELECTION"):
        ipo_hits = scan_ipo_fresh_listings(SCREENER_WATCHLIST[:30])
        if ipo_hits: st.dataframe(pd.DataFrame(ipo_hits), use_container_width=True)

elif menu_selection == "📥 TRANSACTION EXECUTION UNIT":
    st.markdown("### 📥 EXECUTIVE ORDER TRANSITS DESK")
    trade_type = st.radio("Execution Vector:", ["🛒 ACCUMULATE (BUY)", "💰 LIQUIDATE (SELL)"], horizontal=True)
    with st.form("trading_desk_form", clear_on_submit=True):
        stock_name = st.selectbox("Symbol Target", options=sorted(SCREENER_WATCHLIST) if "ACCUMULATE" in trade_type else (sorted(active_portfolio["Stock"].unique()) if not active_portfolio.empty else ["No Active Exposure"]), index=None)
        input_price = st.number_input("Price (INR)", min_value=0.01)
        input_qty = st.number_input("Volume (Qty)", min_value=1)
        trade_date = st.date_input("Ledger Date Seal", datetime.now())
        
        if st.form_submit_button("ROUTE TRANSACTION TARGET TO SYSTEM") and stock_name and stock_name != "No Active Exposure":
            master_df = load_permanent_database()
            if "ACCUMULATE" in trade_type:
                b_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=True)
                if stock_name in master_df[master_df["Status"] == "ACTIVE"]["Stock"].values:
                    idx = master_df[(master_df["Status"] == "ACTIVE") & (master_df["Stock"] == stock_name)].index[0]
                    old_qty = int(master_df.loc[idx, "Quantity"])
                    new_qty = old_qty + input_qty
                    master_df.loc[idx, ["Buy Price", "Quantity", "Buy Charges", "Buy Date"]] = [round(((float(master_df.loc[idx, "Buy Price"]) * old_qty) + (input_price * input_qty)) / new_qty, 2), new_qty, float(master_df.loc[idx, "Buy Charges"]) + b_charges, str(trade_date)]
                else:
                    master_df = pd.concat([master_df, pd.DataFrame([{"Stock": stock_name, "Buy Price": round(input_price, 2), "Quantity": input_qty, "Buy Date": str(trade_date), "Buy Charges": b_charges, "Sell Price": 0.0, "Sell Date": "-", "Sell Charges": 0.0, "Realized P&L": 0.0, "Status": "ACTIVE"}])], ignore_index=True)
            else:
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
                    master_df = pd.concat([master_df, pd.DataFrame([{"Stock": stock_name, "Buy Price": buy_p, "Quantity": input_qty, "Buy Date": master_df.loc[idx, "Buy Date"], "Buy Charges": round(allocated_b_charge, 2), "Sell Price": input_price, "Sell Date": str(trade_date), "Sell Charges": s_charges, "Realized P&L": realized_pnl, "Status": "CLOSED"}])], ignore_index=True)
            
            save_permanent_database(master_df)
            st.rerun()

elif menu_selection == "📋 RUNNING POSITION REPLICA":
    st.markdown("### 📋 ACTIVE RUNNING POSITION INVENTORY")
    if not active_portfolio.empty: st.dataframe(active_portfolio[["Stock", "Quantity", "Buy Price", "Buy Charges", "Buy Date"]], use_container_width=True)

render_operational_guidelines()
render_terminal_footer()
