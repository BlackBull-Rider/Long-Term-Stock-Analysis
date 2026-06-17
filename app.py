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
from core.engine import calculate_indian_market_charges, run_offline_sync_pipeline, load_offline_market_data, scan_ipo_fresh_listings

# Launch HUD Frame Core
apply_terminal_theme()
render_branding_header()

# =========================================================================
# 🦅 100% AUTOMATIC HARD-WRITE GITHUB REPOSITORY DATABASE ENGINE
# =========================================================================
GITHUB_USER = "BlackBull-Rider"
GITHUB_REPO = "Long-Term-Stock-Analysis"
GITHUB_TOKEN = "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"

DB_FILE = "portfolio_db.csv"
API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{DB_FILE}"

def load_permanent_database():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            content = response.json()
            # Base64 ডিকোড করে CSV ডাটা রিড করো
            csv_bytes = base64.b64decode(content["content"])
            df = pd.read_csv(io.BytesIO(csv_bytes))
            df.columns = df.columns.str.strip()
            return df
    except:
        pass
    return pd.DataFrame(columns=[
        "Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges", 
        "Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"
    ])

def save_permanent_database(df):
    """গুগল শিটের কোনো ঝামেলা ছাড়াই সরাসরি গিটহাব রেপোতে অটো-পুশ করার ইঞ্জিন"""
    st.session_state.portfolio_data_store = df
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # গিটহাবে ফাইল রাইট করার আগে কারেন্ট ফাইলের SHA বা ট্র্যাক আইডি নিতে হবে
    sha = None
    try:
        res = requests.get(API_URL, headers=headers, timeout=10)
        if res.status_code == 200:
            sha = res.json()["sha"]
    except:
        pass
        
    csv_string = df.to_csv(index=False)
    # ডাটাকে গিটহাব কমপ্লায়েন্স Base64 ফরম্যাটে এনকোড করো
    encoded_content = base64.b64encode(csv_string.encode("utf-8")).decode("utf-8")
    
    payload = {
        "message": f"🤖 Quant Terminal Auto-Sync // Ledger Modulated {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "content": encoded_content
    }
    if sha:
        payload["sha"] = sha
        
    try:
        response = requests.put(API_URL, headers=headers, json=payload, timeout=15)
        if response.status_code in [200, 201]:
            st.toast("🎯 Portfolio Database Saved Automatically to GitHub!", icon="🦅")
        else:
            st.error("⚠️ GitHub API write restriction. Check Repository Name or Token scopes.")
    except:
        st.error("📡 Git network delay. Transaction cached in running local memory layout.")

# ক্লাউড গিটহাব লাইভ ডেটাবেস সিঙ্ক
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
    raw_df = load_offline_market_data()
    if raw_df.empty:
        st.error("❌ Local Big-Data Cache is empty! Please run 'SYSTEM HARDWARE SYNC' module first.")
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
        st.success(f"🎯 Query processed from offline repository in 0.2 seconds! Isolated: {len(df_final)} matching profiles.")
        st.dataframe(df_final, use_container_width=True)
    else:
        st.warning("No assets matched the exact custom structural formula parameters.")

# =========================================================================
# SYSTEM ENGINE INTELLIGENCE ROUTING
# =========================================================================

if menu_selection == "📊 PORTFOLIO ANALYTICS":
    st.markdown("### 📈 PREMIUM PORTFOLIO EXECUTIVE HUD OVERVIEW")
    if active_portfolio.empty:
        st.info("💡 Portfolio database empty. Route orders via Execution Desk.")
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
        c1.metric("INDEX WEIGHT VALUE", f"{tot_cur:,.2f}", "+1.42% Daily Influx")
        c2.metric("CAPITAL INVESTED", f"₹ {tot_inv:,.2f}")
        c3.metric("CURRENT WALLET EQUITY", f"₹ {tot_cur:,.2f}", delta=f"{roi_pct:.2f}% Real-time Return")
        c4.metric("UNREALIZED MARGIN NET ROI", f"{roi_pct:+.2f}%")

        st.markdown("---")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown("#### 🎯 Capital Asset Allocation Mix")
            fig_pie = px.pie(active_portfolio, names="Stock", values="Current Value", hole=0.4, color_discrete_sequence=px.colors.sequential.Mint_r)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e2e8f0", showlegend=True, margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_pie, use_container_width=True)
        with chart_col2:
            st.markdown("#### 📈 Portfolio Performance Distribution")
            fig_bar = px.bar(active_portfolio, x="Stock", y="Unrealized P&L", color="Unrealized P&L", color_continuous_scale=["#ff3366", "#00ffcc"])
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#e2e8f0", margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")
        st.dataframe(active_portfolio[["Stock", "Quantity", "Buy Price", "CMP (₹)", "Total Invested", "Current Value", "Unrealized P&L"]], use_container_width=True)

elif menu_selection == "🔍 LIVE SCREENER CORE":
    st.subheader("🦅 CORE BATCH QUANT MATRIX")
    col_g1, col_g2 = st.columns(2)
    invest_horizon = col_g1.number_input("Investment Term (Years)", min_value=0.5, max_value=15.0, value=2.0)
    expected_return = col_g2.number_input("Target Expected Return (% p.a.)", min_value=10.0, max_value=150.0, value=25.0)
    
    if expected_return >= 100: calc_sales, calc_roe, calc_pe, calc_ema_dist = 30.0, 35.0, 25.0, 4.0
    elif expected_return >= 60: calc_sales, calc_roe, calc_pe, calc_ema_dist = 22.0, 26.0, 30.0, 3.0
    elif expected_return >= 40: calc_sales, calc_roe, calc_pe, calc_ema_dist = 18.0, 22.0, 35.0, 2.0
    elif expected_return >= 25: calc_sales, calc_roe, calc_pe, calc_ema_dist = 12.0, 15.0, 50.0, 1.0
    else: calc_sales, calc_roe, calc_pe, calc_ema_dist = 10.0, 12.0, 65.0, 0.0

    col_f1, col_f2 = st.columns(2)
    min_sales = col_f1.number_input("Minimum Revenue Growth (%)", value=float(calc_sales))
    min_roe = col_f2.number_input("Minimum Return On Equity (%)", value=float(calc_roe))
    
    col_f3, col_f4 = st.columns(2)
    max_pe = col_f3.number_input("Maximum P/E Ratio Limit", value=float(calc_pe))
    min_mcap = col_f4.number_input("Minimum Market Cap (Cr)", value=1000.0)

    col_o1, col_o2 = st.columns(2)
    min_promoter = col_o1.number_input("Minimum Promoter Ownership (%)", value=35.0)
    min_ema200_dist = col_o2.number_input("Minimum Cushion Space from 200 EMA (%)", value=float(calc_ema_dist))
    
    if st.button("EXECUTE LIVE SCREENER PARALLEL PROCESS"):
        execute_quant_filter_engine(min_sales, min_roe, max_pe, min_mcap, min_promoter, min_ema200_dist)

elif menu_selection == "🚀 MONSTER MOAT HUNT (1000%)":
    st.subheader("🔥 HYPER-MONOPOLY MONSTER MOAT SCANNER")
    col_mg1, col_mg2 = st.columns(2)
    invest_horizon = col_mg1.number_input("Investment Term Sizing (Years)", min_value=0.5, max_value=15.0, value=2.0)
    expected_return = col_mg2.number_input("Alpha Return Target Model (% p.a.)", min_value=10.0, max_value=1500.0, value=120.0)
    
    col_m1, col_m2 = st.columns(2)
    min_gross_margin = col_m1.number_input("Pricing Premium Power (Minimum Gross Margin %)", value=45.0)
    min_inventory_speed = col_m2.number_input("Consumer Velocity Force (Minimum Inventory Speed x)", value=6.0)
    
    col_m3, col_m4 = st.columns(2)
    min_sales = col_m3.number_input("Minimum Sales Growth Rate (%)", value=25.0)
    min_roe = col_m4.number_input("Minimum Operational ROE (%)", value=30.0)
    
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
        execute_quant_filter_engine(
            min_sales, min_roe, max_pe, min_mcap, min_promoter, min_ema200_dist,
            additional_moat_filter=True, gross_m=min_gross_margin, inv_spd=min_inventory_speed,
            inst_val=min_inst, dd_limit=max_dd_limit
        )

elif menu_selection == "📡 SYSTEM HARDWARE SYNC":
    st.markdown("### 🛰️ COLD REPOSITORY DATA SYNC PIPELINE")
    if st.button("⚡ EXECUTE BATCH BULK DATA REPLICATION (CSV SYNC)"):
        with st.spinner("Compiling dynamic listed universes across weekly blocks..."):
            total_synced = run_offline_sync_pipeline(SCREENER_WATCHLIST)
            if total_synced > 0: st.success(f"🔥 SUCCESS! Permanent local repository synced with {total_synced} live profiles!")

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
                    idx = master_df[(master_df["Stock"] == stock_name) & (master_df["Status"] == "ACTIVE")].index[0]
                    old_qty = int(master_df.loc[idx, "Quantity"])
                    new_qty = old_qty + input_qty
                    master_df.loc[idx, ["Buy Price", "Quantity", "Buy Charges", "Buy Date"]] = [round(((float(master_df.loc[idx, "Buy Price"]) * old_qty) + (input_price * input_qty)) / new_qty, 2), new_qty, float(master_df.loc[idx, "Buy Charges"]) + b_charges, str(trade_date)]
                else:
                    master_df = pd.concat([master_df, pd.DataFrame([{"Stock": stock_name, "Buy Price": round(input_price, 2), "Quantity": input_qty, "Buy Date": str(trade_date), "Buy Charges": b_charges, "Sell Price": 0.0, "Sell Date": "-", "Sell Charges": 0.0, "Realized P&L": 0.0, "Status": "ACTIVE"}])], ignore_index=True)
            else:
                idx = master_df[(master_df["Stock"] == stock_name) & (master_df["Status"] == "ACTIVE")].index[0]
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
            
            # 🔥 গিটহাব এপিআই-এর মাধ্যমে সরাসরি রেপোজিটরিতে হার্ড-রাইট পুশ
            save_permanent_database(master_df)
            st.rerun()

elif menu_selection == "📋 RUNNING POSITION REPLICA":
    st.markdown("### 📋 ACTIVE RUNNING POSITION INVENTORY")
    if not active_portfolio.empty: st.dataframe(active_portfolio[["Stock", "Quantity", "Buy Price", "Buy Charges", "Buy Date"]], use_container_width=True)

render_operational_guidelines()
render_terminal_footer()
