# app.py
import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import yfinance as yf
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

from stocks import SCREENER_WATCHLIST
from core.styles import apply_terminal_theme, render_branding_header, render_operational_guidelines, render_terminal_footer
from core.engine import calculate_indian_market_charges, run_massive_scan_engine, scan_ipo_fresh_listings

# Core UI Engine Launcher
apply_terminal_theme()
render_branding_header()

# Permanent File System Settings
DB_FILE = "portfolio_db.csv"

def load_permanent_database():
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            # Standardizing data parsing limits
            if "Current Value" in df.columns: df = df.drop(columns=["Current Value"])
            return df
        except:
            pass
    return pd.DataFrame(columns=[
        "Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges", 
        "Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"
    ])

def save_permanent_database(df):
    df.to_csv(DB_FILE, index=False)

if "portfolio_data_store" not in st.session_state:
    st.session_state.portfolio_data_store = load_permanent_database()

master_df = st.session_state.portfolio_data_store
active_portfolio = master_df[master_df["Status"] == "ACTIVE"].reset_index(drop=True)
closed_portfolio = master_df[master_df["Status"] == "CLOSED"].reset_index(drop=True)

# Main Navigation Layout Channels
st.sidebar.markdown("### 🖥️ QUANT DASHBOARD")
menu_selection = st.sidebar.radio(
    "COMMAND CONTROLLER PANEL",
    [
        "📊 ADVANCED INDUSTRIAL ANALYTICS",
        "🔍 LIVE SCREENER CORE",
        "🚀 MONSTER MOAT HUNT (1000%)",
        "🔮 FRESH IPO MONITOR",
        "📥 TRANSACTION EXECUTION UNIT",
        "📋 RUNNING POSITION REPLICA"
    ]
)

ALL_METRICS_COLS = [
    "Stock", "Chart Setup", "CMP (₹)", "P/E Ratio", "ROE (%)", 
    "Sales Growth (%)", "Gross Margin (%)", "Inventory Speed (x)", 
    "Marketing Efficiency (x)", "Promoter (%)", "Institutions (%)", 
    "Max DD (%)", "EMA200 Dist (%)", "Dividend (%)", "Beta", "System Action"
]

# =========================================================================
# CONTROLLER EXECUTION INTERFACE ROUTER
# =========================================================================

if menu_selection == "📊 ADVANCED INDUSTRIAL ANALYTICS":
    st.markdown("### 📈 PREMIUM PORTFOLIO EXECUTIVE HUD OVERVIEW")
    
    if active_portfolio.empty:
        st.info("💡 Portfolio database is empty. Route orders via the Transaction Execution Unit to view live metric streams.")
    else:
        # ⚡ LIVE STOCK TRACKING PARSER FOR RUNNING ASSETS
        with st.spinner("Syncing core metrics with live market tickers..."):
            tickers_list = [f"{s}.NS" for s in active_portfolio["Stock"].unique()]
            try:
                live_data = yf.download(tickers=tickers_list, period="1d", interval="1m", progress=False)
                last_prices = {}
                for s in active_portfolio["Stock"].unique():
                    tick = f"{s}.NS"
                    if len(tickers_list) > 1:
                        last_prices[s] = float(live_data["Close"][tick].dropna().iloc[-1])
                    else:
                        last_prices[s] = float(live_data["Close"].dropna().iloc[-1])
            except:
                last_prices = {s: float(active_portfolio[active_portfolio["Stock"] == s]["Buy Price"].iloc[0]) for s in active_portfolio["Stock"].unique()}

        # Core Mathematical Formulation Engine
        active_portfolio["CMP (₹)"] = active_portfolio["Stock"].map(last_prices)
        active_portfolio["Total Invested"] = active_portfolio["Quantity"] * active_portfolio["Buy Price"]
        active_portfolio["Current Value"] = active_portfolio["Quantity"] * active_portfolio["CMP (₹)"]
        active_portfolio["Unrealized P&L"] = active_portfolio["Current Value"] - active_portfolio["Total Invested"]
        
        total_invested_capital = active_portfolio["Total Invested"].sum()
        total_current_capital_value = active_portfolio["Current Value"].sum()
        net_unrealized_pnl = total_current_capital_value - total_invested_capital
        total_roi_percentage = (net_unrealized_pnl / total_invested_capital * 100) if total_invested_capital > 0 else 0.0

        # 🌟 RESTORED: Image Reference Layout KPI Glass Cards
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        kpi_col1.metric("INDEX WEIGHT REFERENCE", f"{total_current_capital_value:,.2f}", "+1.42% Daily Change")
        kpi_col2.metric("YOUR CAPITAL INVESTED", f"₹ {total_invested_capital:,.2f}")
        
        pnl_label = f"₹ +{net_unrealized_pnl:,.2f}" if net_unrealized_pnl >= 0 else f"₹ {net_unrealized_pnl:,.2f}"
        kpi_col3.metric("CURRENT PORTFOLIO VALUE", pnl_label, delta=f"{total_roi_percentage:.2f}% Net Return")
        kpi_col4.metric("TOTAL NET UNREALIZED ROI", f"{total_roi_percentage:+.2f}%")

        st.markdown("---")
        
        # 📈 Visual Distribution Charts (Pie allocation system mapping from layout)
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### 🎯 Capital Asset Allocation Mix")
            fig_pie = px.pie(
                active_portfolio, names="Stock", values="Current Value",
                hole=0.4, color_discrete_sequence=px.colors.sequential.Mint_r
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color="#e2e8f0", showlegend=True, margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with chart_col2:
            st.markdown("#### 📈 Portfolio Performance Distribution")
            fig_bar = px.bar(
                active_portfolio, x="Stock", y="Unrealized P&L",
                color="Unrealized P&L", color_continuous_scale=["#ff3366", "#00ffcc"]
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font_color="#e2e8f0", margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 📋 REAL-TIME RUNNING EXPOSURE INSIGHT LEDGER")
        display_portfolio = active_portfolio[["Stock", "Quantity", "Buy Price", "CMP (₹)", "Total Invested", "Current Value", "Unrealized P&L"]]
        st.dataframe(display_portfolio.style.format({
            "Buy Price": "₹{:.2f}", "CMP (₹)": "₹{:.2f}", "Total Invested": "₹{:.2f}",
            "Current Value": "₹{:.2f}", "Unrealized P&L": "₹{:.2f}"
        }), use_container_width=True)

elif menu_selection == "🔍 LIVE SCREENER CORE":
    st.subheader("🦅 CORE BATCH QUANT MATRIX")
    col_g1, col_g2 = st.columns(2)
    invest_horizon = col_g1.number_input("Investment Term (Years)", min_value=0.5, max_value=15.0, value=2.0, step=0.5)
    expected_return = col_g2.number_input("Target Expected Return (% p.a.)", min_value=10.0, max_value=150.0, value=25.0, step=5.0)
    
    if expected_return >= 100: calc_sales, calc_roe, calc_pe, calc_ema_dist = 30.0, 35.0, 25.0, 4.0
    elif expected_return >= 60: calc_sales, calc_roe, calc_pe, calc_ema_dist = 22.0, 26.0, 30.0, 3.0
    elif expected_return >= 40: calc_sales, calc_roe, calc_pe, calc_ema_dist = 18.0, 22.0, 35.0, 2.0
    elif expected_return >= 25: calc_sales, calc_roe, calc_pe, calc_ema_dist = 12.0, 15.0, 50.0, 1.0
    else: calc_sales, calc_roe, calc_pe, calc_ema_dist = 10.0, 12.0, 65.0, 0.0

    calc_mcap = 1500.0 if invest_horizon <= 1.0 else 1000.0
    calc_promoter = 40.0 if expected_return > 35 else 30.0
    
    col_f1, col_f2 = st.columns(2)
    min_sales = col_f1.number_input("Minimum Sales Growth (%)", min_value=0.0, max_value=100.0, value=float(calc_sales))
    min_roe = col_f2.number_input("Minimum ROE (%)", min_value=0.0, max_value=100.0, value=float(calc_roe))
    
    col_f3, col_f4 = st.columns(2)
    max_pe = col_f3.number_input("Maximum P/E Ratio", min_value=0.0, max_value=300.0, value=float(calc_pe))
    min_mcap = col_f4.number_input("Minimum Market Cap (Cr)", min_value=0.0, max_value=500000.0, value=float(calc_mcap))

    col_o1, col_o2 = st.columns(2)
    min_promoter = col_o1.number_input("Minimum Promoter Holding (%)", min_value=0.0, max_value=100.0, value=float(calc_promoter))
    min_ema200_dist = col_o2.number_input("Minimum 200 EMA Distance Cushion (%)", min_value=-50.0, max_value=100.0, value=float(calc_ema_dist))
    
    if st.button("EXECUTE LIVE SCREENER COMPILATION ROUTINE"):
        raw_results = run_massive_scan_engine(SCREENER_WATCHLIST * 10)
        filtered_results = []
        for res in raw_results:
            if not res: continue
            if (res["Sales Growth (%)"] >= min_sales and res["ROE (%)"] >= min_roe and 
                res["Market Cap (Cr)"] >= min_mcap and (max_pe == 0 or res["P/E Ratio"] <= max_pe)):
                if float(res["Promoter (%)"]) >= min_promoter and float(res["EMA200 Dist (%)"]) >= min_ema200_dist:
                    res["EMA200 Dist (%)"] = f"{res['EMA200 Dist (%)']:.1f}%"
                    res["System Action"] = "HOLD" if res["CMP (₹)"] > res["P/E Ratio"] else "ACCUMULATE"
                    filtered_results.append(res)
        if filtered_results:
            st.dataframe(pd.DataFrame(filtered_results)[ALL_METRICS_COLS], use_container_width=True)

elif menu_selection == "🚀 MONSTER MOAT HUNT (1000%)":
    st.subheader("🔥 HYPER-MONOPOLY BRAND MOAT CATALYST SCREENERS")
    col_mg1, col_mg2 = st.columns(2)
    invest_horizon = col_mg1.number_input("Investment Term Sizing (Years)", min_value=0.5, max_value=15.0, value=2.0, step=0.5, key="moat_horizon")
    expected_return = col_mg2.number_input("Alpha Return Target Model (% p.a.)", min_value=10.0, max_value=1500.0, value=120.0, step=5.0, key="moat_return")
    
    if expected_return >= 500: m_sales, m_roe, m_pe, m_dist, m_prom = 45.0, 50.0, 15.0, 5.0, 45.0
    elif expected_return >= 150: m_sales, m_roe, m_pe, m_dist, m_prom = 35.0, 40.0, 20.0, 4.0, 45.0
    elif expected_return >= 80: m_sales, m_roe, m_pe, m_dist, m_prom = 25.0, 30.0, 30.0, 3.0, 40.0
    elif expected_return >= 40: m_sales, m_roe, m_pe, m_dist, m_prom = 15.0, 20.0, 45.0, 1.5, 40.0
    else: m_sales, m_roe, m_pe, m_dist, m_prom = 10.0, 12.0, 60.0, 0.0, 35.0

    m_mcap = 2000.0 if invest_horizon <= 1.0 else 1000.0
    
    col_m1, col_m2 = st.columns(2)
    min_gross_margin = col_m1.number_input("Pricing Monopolistic Premium (Minimum Gross Margin %)", min_value=20.0, max_value=90.0, value=45.0)
    min_inventory_speed = col_m2.number_input("FMCG/Consumer Velocity Scale (Minimum Inventory Speed x)", min_value=2.0, max_value=25.0, value=6.0)
    
    col_m3, col_m4 = st.columns(2)
    min_sales = col_m3.number_input("Minimum Revenue Acceleration Rate (%)", min_value=0.0, max_value=100.0, value=m_sales)
    min_roe = col_m4.number_input("Minimum Operational Capital ROE (%)", min_value=0.0, max_value=100.0, value=m_roe)
    
    col_m5, col_m6 = st.columns(2)
    max_pe = col_m5.number_input("Maximum Multiples Cap Limit", min_value=0.0, max_value=300.0, value=m_pe)
    min_mcap = col_m6.number_input("Minimum Threshold Market Cap (Cr)", min_value=0.0, max_value=500000.0, value=m_mcap)

    col_m7, col_m8 = st.columns(2)
    min_promoter = col_m7.number_input("Minimum Promoter Base Block Ownership (%)", min_value=0.0, max_value=100.0, value=m_prom)
    min_ema200_dist = col_m8.number_input("Minimum Cushion Space Target from 200 EMA (%)", min_value=-50.0, max_value=100.0, value=m_dist)

    col_mx1, col_mx2 = st.columns(2)
    min_inst = col_mx1.number_input("Minimum Institutional FII Allocation Layer (%)", min_value=0.0, max_value=100.0, value=10.0)
    max_dd_limit = col_mx2.number_input("Maximum Operational Peak Drawdown Boundary (%)", min_value=-95.0, max_value=0.0, value=-50.0)
    
    if st.button("EXECUTE MONSTER MOAT INSIGHT CORES"):
        raw_results = run_massive_scan_engine(SCREENER_WATCHLIST * 10)
        moat_hits = []
        for res in raw_results:
            if not res: continue
            if (res["Gross Margin (%)"] >= min_gross_margin and res["Inventory Speed (x)"] >= min_inventory_speed and
                res["Sales Growth (%)"] >= min_sales and res["ROE (%)"] >= min_roe and 
                res["Market Cap (Cr)"] >= min_mcap and (max_pe == 0 or res["P/E Ratio"] <= max_pe) and
                res["Institutions (%)"] >= min_inst and res["Max DD (%)"] >= max_dd_limit):
                if float(res["Promoter (%)"]) >= min_promoter and float(res["EMA200 Dist (%)"]) >= min_ema200_dist:
                    res["EMA200 Dist (%)"] = f"{res['EMA200 Dist (%)']:.1f}%"
                    res["System Action"] = "HOLD"
                    moat_hits.append(res)
        if moat_hits:
            st.dataframe(pd.DataFrame(moat_hits)[ALL_METRICS_COLS], use_container_width=True)

elif menu_selection == "🔮 FRESH IPO MONITOR":
    st.markdown("### 🌌 NEW LISTINGS AREA")
    if st.button("RUN IPO MONITOR SEQUENCER"):
        ipo_hits = scan_ipo_fresh_listings(SCREENER_WATCHLIST[:15])
        if ipo_hits: st.dataframe(pd.DataFrame(ipo_hits), use_container_width=True)

elif menu_selection == "📥 TRANSACTION EXECUTION UNIT":
    st.markdown("### 📡 HIGH-SPEED TRANSACTION ROUTING LAYER")
    trade_type = st.radio("Execution Path Vector:", ["🛒 ACCUMULATE FRESH RISK (BUY)", "💰 LIQUIDATE EXPOSURE (SELL)"], horizontal=True)
    with st.form("trading_desk_form", clear_on_submit=True):
        if "ACCUMULATE" in trade_type:
            stock_name = st.selectbox("Select Target Ticker Symbol", options=sorted(SCREENER_WATCHLIST), index=None)
        else:
            stock_name = st.selectbox("Select Active Risk Inventory to Liquidate", options=sorted(active_portfolio["Stock"].unique()) if not active_portfolio.empty else ["No Active Exposure"], index=None)
        input_price = st.number_input("Execution Matrix Price (INR)", min_value=0.01, step=0.1)
        input_qty = st.number_input("Execution Volume Sizing (Qty)", min_value=1, step=1)
        trade_date = st.date_input("Transaction Ledger Date Seal", datetime.now())
        
        if st.form_submit_button("ROUTE TRANSACTION TARGET TO SYSTEM"):
            if stock_name and stock_name != "No Active Exposure":
                master_df = load_permanent_database()
                if "ACCUMULATE" in trade_type:
                    b_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=True)
                    if stock_name in master_df[master_df["Status"] == "ACTIVE"]["Stock"].values:
                        idx = master_df[(master_df["Stock"] == stock_name) & (master_df["Status"] == "ACTIVE")].index[0]
                        old_qty = int(master_df.loc[idx, "Quantity"])
                        old_price = float(master_df.loc[idx, "Buy Price"])
                        old_charges = float(master_df.loc[idx, "Buy Charges"])
                        new_qty = old_qty + input_qty
                        new_avg_price = ((old_price * old_qty) + (input_price * input_qty)) / new_qty
                        master_df.loc[idx, ["Buy Price", "Quantity", "Buy Charges", "Buy Date"]] = [round(new_avg_price, 2), new_qty, old_charges + b_charges, str(trade_date)]
                    else:
                        new_row = pd.DataFrame([{
                            "Stock": stock_name, "Buy Price": round(input_price, 2), "Quantity": input_qty, 
                            "Buy Date": str(trade_date), "Buy Charges": b_charges, "Sell Price": 0.0, 
                            "Sell Date": "-", "Sell Charges": 0.0, "Realized P&L": 0.0, "Status": "ACTIVE"
                        }])
                        master_df = pd.concat([master_df, new_row], ignore_index=True)
                    save_permanent_database(master_df)
                    st.success("Transaction localized successfully.")
                    st.rerun()
                else:
                    idx = master_df[(master_df["Stock"] == stock_name) & (master_df["Status"] == "ACTIVE")].index[0]
                    old_qty = int(master_df.loc[idx, "Quantity"])
                    buy_p = float(master_df.loc[idx, "Buy Price"])
                    b_charges = float(master_df.loc[idx, "Buy Charges"])
                    s_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=False)
                    allocated_buy_charge = b_charges * (input_qty / old_qty)
                    realized_pnl = round(((input_price - buy_p) * input_qty) - (allocated_buy_charge + s_charges), 2)
                    if input_qty >= old_qty:
                        master_df.loc[idx, ["Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"]] = [input_price, str(trade_date), s_charges, realized_pnl, "CLOSED"]
                    else:
                        master_df.loc[idx, "Quantity"] = old_qty - input_qty
                        master_df.loc[idx, "Buy Charges"] = b_charges - allocated_buy_charge
                        partial_closed_row = pd.DataFrame([{
                            "Stock": stock_name, "Buy Price": buy_p, "Quantity": input_qty, "Buy Date": master_df.loc[idx, "Buy Date"], 
                            "Buy Charges": round(allocated_buy_charge, 2), "Sell Price": input_price, "Sell Date": str(trade_date), "Sell Charges": s_charges, "Realized P&L": realized_pnl, "Status": "CLOSED"
                        }])
                        master_df = pd.concat([master_df, partial_closed_row], ignore_index=True)
                    save_permanent_database(master_df)
                    st.success("Liquidation localized successfully.")
                    st.rerun()

elif menu_selection == "📋 RUNNING POSITION REPLICA":
    st.markdown("### 📋 ACTIVE RISK INVENTORY ANALYSIS LEDGER")
    active_portfolio = load_permanent_database()
    active_portfolio = active_portfolio[active_portfolio["Status"] == "ACTIVE"].reset_index(drop=True)
    if not active_portfolio.empty:
        st.dataframe(active_portfolio[["Stock", "Quantity", "Buy Price", "Buy Charges", "Buy Date"]], use_container_width=True)

render_operational_guidelines()
render_terminal_footer()
