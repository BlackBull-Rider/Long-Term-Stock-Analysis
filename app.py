# app.py
import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

from stocks import SCREENER_WATCHLIST
from core.styles import apply_terminal_theme, render_branding_header, render_operational_guidelines, render_terminal_footer
from core.engine import calculate_indian_market_charges, run_massive_scan_engine, scan_ipo_fresh_listings

# Core UI Launcher
apply_terminal_theme()
render_branding_header()

# 💾 [PERMANENT FILE DATABASE CORES] - রিফ্রেশ করলেও ডেটা মুছবে না
DB_FILE = "portfolio_db.csv"

def load_permanent_database():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            pass
    # ফাইল না থাকলে ব্ল্যাঙ্ক স্ট্রাকচার তৈরি হবে
    return pd.DataFrame(columns=[
        "Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges", 
        "Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"
    ])

def save_permanent_database(df):
    df.to_csv(DB_FILE, index=False)

# প্রথমে ফাইল থেকে পুরনো ডেটা লোড করো
if "portfolio_data_store" not in st.session_state:
    st.session_state.portfolio_data_store = load_permanent_database()

# True Session-State Reactive Memory Matrix for Moat
if "moat_sales" not in st.session_state: st.session_state.moat_sales = 15.0
if "moat_roe" not in st.session_state: st.session_state.moat_roe = 20.0
if "moat_pe" not in st.session_state: st.session_state.moat_pe = 45.0
if "moat_mcap" not in st.session_state: st.session_state.moat_mcap = 1000.0
if "moat_promoter" not in st.session_state: st.session_state.moat_promoter = 40.0
if "moat_dist" not in st.session_state: st.session_state.moat_dist = 1.5

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

ALL_METRICS_COLS = [
    "Stock", "Chart Setup", "CMP (₹)", "P/E Ratio", "ROE (%)", 
    "Sales Growth (%)", "Gross Margin (%)", "Inventory Speed (x)", 
    "Marketing Efficiency (x)", "Promoter (%)", "Institutions (%)", 
    "Max DD (%)", "EMA200 Dist (%)", "Dividend (%)", "Beta", "System Action"
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
        
        raw_results = run_massive_scan_engine(SCREENER_WATCHLIST * 10)
        filtered_results = []
        
        for res in raw_results:
            if not res: continue
            if (res["Sales Growth (%)"] >= min_sales and res["ROE (%)"] >= min_roe and 
                res["Market Cap (Cr)"] >= min_mcap and (max_pe == 0 or res["P/E Ratio"] <= max_pe)):
                
                if float(res["Promoter (%)"]) >= min_promoter and float(res["EMA200 Dist (%)"]) >= min_ema200_dist:
                    res["EMA200 Dist (%)"] = f"{res['EMA200 Dist (%)']:.1f}%"
                    valuation_tag = "DISCOUNTED BASE" if res["P/E Ratio"] < max_pe else "PREMIUM VALUE"
                    res["Stock"] = f"{res['Stock']} [{valuation_tag}]"
                    res["System Action"] = "HOLD" if res["CMP (₹)"] > res["EMA50"] else "BOOK 50%"
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
    
    col_mg1, col_mg2 = st.columns(2)
    invest_horizon = col_mg1.number_input("Investment Term (Years)", min_value=0.5, max_value=15.0, value=2.0, step=0.5, key="moat_horizon")
    expected_return = col_mg2.number_input("Target Expected Return (% p.a.)", min_value=10.0, max_value=1500.0, value=120.0, step=5.0, key="moat_return")
    
    if expected_return >= 500:
        m_sales, m_roe, m_pe, m_dist, m_prom = 45.0, 50.0, 15.0, 5.0, 45.0
    elif expected_return >= 150:
        m_sales, m_roe, m_pe, m_dist, m_prom = 35.0, 40.0, 20.0, 4.0, 45.0
    elif expected_return >= 80:
        m_sales, m_roe, m_pe, m_dist, m_prom = 25.0, 30.0, 30.0, 3.0, 40.0
    elif expected_return >= 40:
        m_sales, m_roe, m_pe, m_dist, m_prom = 15.0, 20.0, 45.0, 1.5, 40.0
    else:
        m_sales, m_roe, m_pe, m_dist, m_prom = 10.0, 12.0, 60.0, 0.0, 35.0

    m_mcap = 2000.0 if invest_horizon <= 1.0 else 1000.0
    
    col_m1, col_m2 = st.columns(2)
    min_gross_margin = col_m1.number_input("Brand Pricing Premium Power (Minimum Gross Margin %)", min_value=20.0, max_value=90.0, value=45.0)
    min_inventory_speed = col_m2.number_input("Consumer Velocity Force (Minimum Inventory Speed x)", min_value=2.0, max_value=25.0, value=6.0)
    
    col_m3, col_m4 = st.columns(2)
    min_sales = col_m3.number_input("Minimum Sales Growth (%)", min_value=0.0, max_value=100.0, value=m_sales)
    min_roe = col_m4.number_input("Minimum ROE (%)", min_value=0.0, max_value=100.0, value=m_roe)
    
    col_m5, col_m6 = st.columns(2)
    max_pe = col_m5.number_input("Maximum P/E Ratio (0 for Any)", min_value=0.0, max_value=300.0, value=m_pe)
    min_mcap = col_m6.number_input("Minimum Market Cap (Cr)", min_value=0.0, max_value=500000.0, value=m_mcap)

    col_m7, col_m8 = st.columns(2)
    min_promoter = col_m7.number_input("Minimum Promoter Holding (%)", min_value=0.0, max_value=100.0, value=m_prom)
    min_ema200_dist = col_m8.number_input("Minimum 200 EMA Cushion Distance (%)", min_value=-50.0, max_value=100.0, value=m_dist)

    col_mx1, col_mx2 = st.columns(2)
    min_inst = col_mx1.number_input("Minimum Institutional Allocation (%)", min_value=0.0, max_value=100.0, value=10.0)
    max_dd_limit = col_mx2.number_input("Maximum Allowed Peak Drawdown (%)", min_value=-95.0, max_value=0.0, value=-50.0)
    
    if st.button("RUN 1000% MULTIBAGGER INSIGHT ENGINE"):
        status = st.empty()
        status.warning("Analyzing brand loyalty indices and structural multi-year breakout parameters...")
        
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
                    valuation_tag = "DISCOUNTED BASE" if res["P/E Ratio"] < max_pe else "PREMIUM VALUE"
                    res["Stock"] = f"{res['Stock']} [{valuation_tag}]"
                    res["System Action"] = "HOLD" if res["CMP (₹)"] > res["EMA50"] else "BOOK 50%"
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
    trade_type = st.radio("Execution Vector:", ["🛒 ACCUMULATE (BUY/TOP-UP)", "💰 LIQUIDATE (SELL/REDUCE)"], horizontal=True)
    
    with st.form("trading_desk_form", clear_on_submit=True):
        if "ACCUMULATE" in trade_type:
            stock_name = st.selectbox("Select Asset Symbol", options=sorted(SCREENER_WATCHLIST), index=None)
        else:
            stock_name = st.selectbox("Select Active Asset to Liquidate", options=sorted(active_portfolio["Stock"].unique()) if not active_portfolio.empty else ["No Active Exposure"], index=None)
            
        input_price = st.number_input("Execution Price (INR)", min_value=0.01, step=0.1)
        input_qty = st.number_input("Volume Order Size (Qty)", min_value=1, step=1)
        trade_date = st.date_input("Transaction Log Date", datetime.now())
        
        if st.form_submit_button("ROUTE TRANSACTION TARGET TO SYSTEM"):
            if stock_name and stock_name != "No Active Exposure":
                master_df = load_permanent_database() # ডাইরেক্ট হার্ডডিস্ক ফাইল থেকে কারেন্ট ডাটা তোলো
                
                if "ACCUMULATE" in trade_type:
                    b_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=True)
                    
                    if stock_name in master_df[master_df["Status"] == "ACTIVE"]["Stock"].values:
                        idx = master_df[(master_df["Stock"] == stock_name) & (master_df["Status"] == "ACTIVE")].index[0]
                        old_qty = int(master_df.loc[idx, "Quantity"])
                        old_price = float(master_df.loc[idx, "Buy Price"])
                        old_charges = float(master_df.loc[idx, "Buy Charges"])
                        
                        new_qty = old_qty + input_qty
                        new_avg_price = ((old_price * old_qty) + (input_price * input_qty)) / new_qty
                        
                        master_df.loc[idx, ["Buy Price", "Quantity", "Buy Charges", "Buy Date"]] = [
                            round(new_avg_price, 2), new_qty, old_charges + b_charges, str(trade_date)
                        ]
                    else:
                        new_row = pd.DataFrame([{
                            "Stock": stock_name, "Buy Price": round(input_price, 2), "Quantity": input_qty, 
                            "Buy Date": str(trade_date), "Buy Charges": b_charges, "Sell Price": 0.0, 
                            "Sell Date": "-", "Sell Charges": 0.0, "Realized P&L": 0.0, "Status": "ACTIVE"
                        }])
                        master_df = pd.concat([master_df, new_row], ignore_index=True)
                        
                    save_permanent_database(master_df) # 💾 সঙ্গে সঙ্গে ফাইলে পার্মানেন্ট সেভ করো
                    st.session_state.portfolio_data_store = master_df
                    st.success(f"Position saved permanently to file database! Total Tax: ₹{b_charges}")
                    st.rerun()
                    
                else:
                    idx = master_df[(master_df["Stock"] == stock_name) & (master_df["Status"] == "ACTIVE")].index[0]
                    old_qty = int(master_df.loc[idx, "Quantity"])
                    buy_p = float(master_df.loc[idx, "Buy Price"])
                    b_date = master_df.loc[idx, "Buy Date"]
                    b_charges = float(master_df.loc[idx, "Buy Charges"])
                    
                    s_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=False)
                    allocated_buy_charge = b_charges * (input_qty / old_qty)
                    realized_pnl = ((input_price - buy_p) * input_qty) - (allocated_buy_charge + s_charges)
                    
                    if input_qty >= old_qty:
                        master_df.loc[idx, ["Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"]] = [
                            input_price, str(trade_date), s_charges, round(realized_pnl, 2), "CLOSED"
                        ]
                    else:
                        master_df.loc[idx, "Quantity"] = old_qty - input_qty
                        master_df.loc[idx, "Buy Charges"] = b_charges - allocated_buy_charge
                        
                        partial_closed_row = pd.DataFrame([{
                            "Stock": stock_name, "Buy Price": buy_p, "Quantity": input_qty, "Buy Date": b_date, 
                            "Buy Charges": round(allocated_buy_charge, 2), "Sell Price": input_price, 
                            "Sell Date": str(trade_date), "Sell Charges": s_charges, "Realized P&L": round(realized_pnl, 2), "Status": "CLOSED"
                        }])
                        master_df = pd.concat([master_df, partial_closed_row], ignore_index=True)
                        
                    save_permanent_database(master_df) # 💾 সঙ্গে সঙ্গে ফাইলে পার্মানেন্ট সেভ করো
                    st.session_state.portfolio_data_store = master_df
                    st.success(f"Position updated & locked in database! Net Cash P&L booked: ₹{realized_pnl:,.2f}")
                    st.rerun()

elif menu_selection == "📋 RUNNING POSITION REPLICA":
    st.subheader("📋 REPLICA ACCOUNTING SYSTEM PORTFOLIO")
    active_portfolio = load_permanent_database()
    active_portfolio = active_portfolio[active_portfolio["Status"] == "ACTIVE"].reset_index(drop=True)
    
    if active_portfolio.empty:
        st.info("System layer vacant. Append positions using Transaction Desk.")
    else:
        st.dataframe(active_portfolio[["Stock", "Quantity", "Buy Price", "Buy Charges", "Buy Date"]], use_container_width=True)
        
        csv_active = active_portfolio.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DOWNLOAD RUNNING PORTFOLIO REAL-TIME LEDGER",
            data=csv_active,
            file_name=f"running_portfolio_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

elif menu_selection == "📊 RISK ASSESSMENT MODULE":
    st.subheader("📊 DEEP QUANT PORTFOLIO METRICS & CLOSED ARCHIVES")
    db_data = load_permanent_database()
    active_p = db_data[db_data["Status"] == "ACTIVE"]
    closed_p = db_data[db_data["Status"] == "CLOSED"]
    
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Total Active Assets Tracked", len(active_p))
    col_m2.metric("Total Closed Book Trades", len(closed_p))
    
    if closed_p.empty:
        st.info("No closed historical records found inside session storage layers.")
    else:
        st.markdown("### CLOSED REVENUE TRANSACTION HISTORY")
        st.dataframe(closed_p[["Stock", "Quantity", "Buy Price", "Sell Price", "Realized P&L", "Sell Date"]], use_container_width=True)
        st.metric("Net Cumulative Closed Cash P&L", f"₹{closed_p['Realized P&L'].sum():,.2f}")
        
        csv_closed = closed_p.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DOWNLOAD CLOSED HISTORICAL LEDGER VAULT",
            data=csv_closed,
            file_name=f"closed_history_vault_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Layout Tips Injection
render_operational_guidelines()
render_terminal_footer()
