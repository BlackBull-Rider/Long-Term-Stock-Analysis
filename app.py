# app.py
import streamlit as st
import pandas as pd
import random
from datetime import datetime

from stocks import SCREENER_WATCHLIST
from core.styles import apply_terminal_theme, render_branding_header, render_operational_guidelines, render_terminal_footer
from core.engine import calculate_indian_market_charges, run_massive_scan_engine, scan_ipo_fresh_listings

# Core UI Launcher
apply_terminal_theme()
render_branding_header()

if "portfolio_data_store" not in st.session_state:
    st.session_state.portfolio_data_store = pd.DataFrame(columns=[
        "Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges", 
        "Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"
    ])

master_df = st.session_state.portfolio_data_store
active_portfolio = master_df[master_df["Status"] == "ACTIVE"].reset_index(drop=True)
closed_portfolio = master_df[master_df["Status"] == "CLOSED"].reset_index(drop=True)

# Master Layout Sidebar Controls
st.sidebar.title("🦅 MASTER NAVIGATION")
st.sidebar.write("`IDENTITY: GREEN BULL RIDER`")
st.sidebar.markdown("---")

menu_selection = st.sidebar.radio(
    "CHOOSE MODULE PLATFORM",
    [
        "🔍 LIVE SCREENER CORE",
        "🚀 MONSTER MOAT HUNT (1000%)",
        "⚡ FRESH IPO MONITOR",
        "📥 TRANSACTION EXECUTION UNIT",
        "📋 RUNNING POSITION REPLICA",
        "📊 RISK ASSESSMENT MODULE"
    ]
)

# Automated Sidebar Wisdom Carousel Module
st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Fund Manager Wisdom")
quotes = [
    "“FIIs and Promoters dictate the macro direction; retail volume just fills the gaps.”",
    "“Fundamentals tell you WHAT to buy. Technicals tell you WHEN to buy.”",
    "“Amateurs think about how much money they can make. Professionals think about how much they could lose.”",
    "“Price follows earnings. If net profit margins expand, multi-year breakouts follow.”",
    "“Bypassing direct exchange paths prevents network tracking. Cache computing is security.”"
]
st.sidebar.warning(random.choice(quotes))

# Complete Operational Column Framework
ALL_METRICS_COLS = [
    "Stock", "Chart Setup", "CMP (₹)", "P/E Ratio", "ROE (%)", 
    "Sales Growth (%)", "Gross Margin (%)", "Inventory Speed (x)", 
    "Marketing Efficiency (x)", "Promoter (%)", "Institutions (%)", 
    "Max DD (%)", "EMA200 Dist (%)", "System Action"
]

# =========================================================================
# CONTROLLER BRANCH ROUTING ENGINE
# =========================================================================

if menu_selection == "🔍 LIVE SCREENER CORE":
    st.subheader("🦅 CORE BATCH QUANT MATRIX")
    
    col_g1, col_g2 = st.columns(2)
    invest_horizon = col_g1.number_input("Investment Term (Years)", min_value=0.5, max_value=15.0, value=2.0, step=0.5)
    expected_return = col_g2.number_input("Target Expected Return (% p.a.)", min_value=10.0, max_value=150.0, value=25.0, step=5.0)
    
    if expected_return >= 100:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 30.0, 35.0, 25.0, 4.0
    elif expected_return >= 60:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 22.0, 26.0, 30.0, 3.0
    elif expected_return >= 40:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 18.0, 22.0, 35.0, 2.0
    elif expected_return >= 25:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 12.0, 15.0, 50.0, 1.0
    else:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 10.0, 12.0, 65.0, 0.0

    calc_mcap = 1500.0 if invest_horizon <= 1.0 else 1000.0
    calc_promoter = 40.0 if expected_return > 35 else 30.0
    
    col_f1, col_f2 = st.columns(2)
    min_sales = col_f1.number_input("Minimum Sales Growth (%)", min_value=0.0, max_value=100.0, value=float(calc_sales))
    min_roe = col_f2.number_input("Minimum ROE (%)", min_value=0.0, max_value=100.0, value=float(calc_roe))
    
    col_f3, col_f4 = st.columns(2)
    max_pe = col_f3.number_input("Maximum P/E Ratio (0 for Any)", min_value=0.0, max_value=300.0, value=float(calc_pe))
    min_mcap = col_f4.number_input("Minimum Market Cap (Cr)", min_value=0.0, max_value=500000.0, value=float(calc_mcap))

    col_o1, col_o2 = st.columns(2)
    min_promoter = col_o1.number_input("Minimum Promoter Holding (%)", min_value=0.0, max_value=100.0, value=float(calc_promoter))
    min_ema200_dist = col_o2.number_input("Minimum 200 EMA Cushion Distance (%)", min_value=-50.0, max_value=100.0, value=float(calc_ema_dist))
    
    if st.button("EXECUTE LIVE SCREENER PARALLEL PROCESS"):
        status_box = st.empty()
        status_box.info("Syncing cached 7-year pipeline records...")
        
        raw_results = run_massive_scan_engine(SCREENER_WATCHLIST * 10, invest_horizon, expected_return)
        filtered_results = []
        
        for res in raw_results:
            if not res: continue
            if (res["Sales Growth (%)"] >= min_sales and res["ROE (%)"] >= min_roe and 
                res["Market Cap (Cr)"] >= min_mcap and (max_pe == 0 or res["P/E Ratio"] <= max_pe)):
                
                if float(res["Promoter (%)"]) >= min_promoter and float(res["EMA200 Dist (%)"].replace("%","")) >= min_ema200_dist:
                    filtered_results.append(res)
                    
        status_box.empty()
        if filtered_results:
            st.success(f"Execution complete. Filtered {len(filtered_results)} matching assets.")
            df_final = pd.DataFrame(filtered_results)[ALL_METRICS_COLS]
            st.dataframe(df_final, use_container_width=True)
            
            st.markdown("---")
            csv_data = df_final.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 DOWNLOAD FILTERED WATCHLIST (CSV SHEET)",
                data=csv_data,
                file_name=f"core_screener_alpha_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

elif menu_selection == "🚀 MONSTER MOAT HUNT (1000%)":
    st.subheader("🔥 HYPER-MONOPOLY MONSTER MOAT SCANNER")
    
    # Core Macro Goals (Target Ceiling Extended to 1500%!)
    col_mg1, col_mg2 = st.columns(2)
    invest_horizon = col_mg1.number_input("Investment Term (Years)", min_value=0.5, max_value=15.0, value=2.0, step=0.5, key="moat_horizon")
    expected_return = col_mg2.number_input("Target Expected Return (% p.a.)", min_value=10.0, max_value=1500.0, value=50.0, step=5.0, key="moat_return")
    
    # 🧠 Dynamic Auto-Parameter Calculation Matrix for Moat Platform
    if expected_return >= 500:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 45.0, 50.0, 15.0, 5.0
    elif expected_return >= 150:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 35.0, 40.0, 20.0, 4.0
    elif expected_return >= 80:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 25.0, 30.0, 30.0, 3.0
    elif expected_return >= 40:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 15.0, 20.0, 45.0, 1.5
    else:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 10.0, 12.0, 60.0, 0.0

    calc_mcap = 2000.0 if invest_horizon <= 1.0 else 1000.0
    calc_promoter = 45.0 if expected_return > 50 else 35.0
    
    # 🚀 Fully Exposed Moat Parameter Controls Block (Linked dynamically to variables!)
    col_m1, col_m2 = st.columns(2)
    min_gross_margin = col_m1.number_input("Brand Pricing Premium Power (Minimum Gross Margin %)", min_value=20.0, max_value=90.0, value=45.0)
    min_inventory_speed = col_m2.number_input("Consumer Velocity Force (Minimum Inventory Speed x)", min_value=2.0, max_value=25.0, value=6.0)
    
    col_m3, col_m4 = st.columns(2)
    min_sales = col_m3.number_input("Minimum Sales Growth (%)", min_value=0.0, max_value=100.0, value=float(calc_sales), key="moat_sales")
    min_roe = col_m4.number_input("Minimum ROE (%)", min_value=0.0, max_value=100.0, value=float(calc_roe), key="moat_roe")
    
    col_m5, col_m6 = st.columns(2)
    max_pe = col_m5.number_input("Maximum P/E Ratio (0 for Any)", min_value=0.0, max_value=300.0, value=float(calc_pe), key="moat_pe")
    min_mcap = col_m6.number_input("Minimum Market Cap (Cr)", min_value=0.0, max_value=500000.0, value=float(calc_mcap), key="moat_mcap")

    col_m7, col_m8 = st.columns(2)
    min_promoter = col_m7.number_input("Minimum Promoter Holding (%)", min_value=0.0, max_value=100.0, value=float(calc_promoter), key="moat_promoter")
    min_ema200_dist = col_m8.number_input("Minimum 200 EMA Cushion Distance (%)", min_value=-50.0, max_value=100.0, value=float(calc_ema_dist), key="moat_dist")
    
    if st.button("RUN 1000% MULTIBAGGER INSIGHT ENGINE"):
        status = st.empty()
        status.warning("Analyzing brand loyalty indices and structural multi-year breakout parameters...")
        
        raw_results = run_massive_scan_engine(SCREENER_WATCHLIST * 10, invest_horizon, expected_return)
        moat_hits = []
        
        for res in raw_results:
            if not res: continue
            if (res["Gross Margin (%)"] >= min_gross_margin and res["Inventory Speed (x)"] >= min_inventory_speed and
                res["Sales Growth (%)"] >= min_sales and res["ROE (%)"] >= min_roe and 
                res["Market Cap (Cr)"] >= min_mcap and (max_pe == 0 or res["P/E Ratio"] <= max_pe)):
                
                if float(res["Promoter (%)"]) >= min_promoter and float(res["EMA200 Dist (%)"].replace("%","")) >= min_ema200_dist:
                    moat_hits.append(res)
                    
        status.empty()
        if moat_hits:
            st.success(f"Moat configuration complete. Found {len(moat_hits)} high-alpha compounds.")
            df_moat_final = pd.DataFrame(moat_hits)[ALL_METRICS_COLS]
            st.dataframe(df_moat_final, use_container_width=True)
            
            st.markdown("---")
            csv_moat = df_moat_final.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 DOWNLOAD MONSTER MOAT DATASET (CSV SHEET)",
                data=csv_moat,
                file_name=f"monster_moat_alpha_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.error("No core asset matched these strict structural parameters.")

elif menu_selection == "⚡ FRESH IPO MONITOR":
    st.subheader("🚀 FRESH LISTINGS BREAKOUT TRACKER")
    if st.button("SCAN FRESH IPO VOLUME INFLEXIONS"):
        ipo_hits = scan_ipo_fresh_listings(SCREENER_WATCHLIST[:15])
        if ipo_hits: 
            df_ipo = pd.DataFrame(ipo_hits)
            st.dataframe(df_ipo, use_container_width=True)
            
            csv_ipo = df_ipo.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 DOWNLOAD FRESH IPO SELECTION (CSV SHEET)",
                data=csv_ipo,
                file_name=f"ipo_breakout_alpha_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

elif menu_selection == "📥 TRANSACTION EXECUTION UNIT":
    st.subheader("📥 TRADING DESK EXECUTION FRAMEWORK")
    with st.form("trading_desk_form", clear_on_submit=True):
        stock_name = st.selectbox("Select Asset Symbol", options=sorted(SCREENER_WATCHLIST), index=None)
        input_price = st.number_input("Execution Price (INR)", min_value=0.1)
        input_qty = st.number_input("Volume Order Size", min_value=1)
        trade_date = st.date_input("Date", datetime.now())
        
        if st.form_submit_button("ROUTE TRANSACTION TARGET TO SYSTEM") and stock_name:
            b_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=True)
            new_row = pd.DataFrame([{
                "Stock": stock_name, "Buy Price": input_price, "Quantity": input_qty, 
                "Buy Date": str(trade_date), "Buy Charges": b_charges, "Sell Price": 0.0, 
                "Sell Date": "-", "Sell Charges": 0.0, "Realized P&L": 0.0, "Status": "ACTIVE"
            }])
            st.session_state.portfolio_data_store = pd.concat([st.session_state.portfolio_data_store, new_row], ignore_index=True)
            st.success("Transaction Processed Successfully into Account Replica Layout!")

elif menu_selection == "📋 RUNNING POSITION REPLICA":
    st.subheader("📋 REPLICA ACCOUNTING SYSTEM PORTFOLIO")
    if active_portfolio.empty:
        st.info("System layer vacant. Append positions using Transaction Desk.")
    else:
        st.dataframe(active_portfolio, use_container_width=True)
        
        csv_active = active_portfolio.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DOWNLOAD RUNNING PORTFOLIO REAL-TIME LEDGER",
            data=csv_active,
            file_name=f"running_portfolio_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

elif menu_selection == "📊 RISK ASSESSMENT MODULE":
    st.subheader("📊 DEEP QUANT PORTFOLIO METRICS & CLOSED ARCHIVES")
    if closed_portfolio.empty:
        st.info("No historical archives found to compute closed account logs.")
    else:
        st.markdown("### CLOSED REVENUE TRANSACTION HISTORY")
        st.dataframe(closed_portfolio, use_container_width=True)
        
        csv_closed = closed_portfolio.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DOWNLOAD CLOSED HISTORICAL LEDGER VAULT",
            data=csv_closed,
            file_name=f"closed_history_vault_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Layout Tips Injection
render_operational_guidelines()
render_terminal_footer()
