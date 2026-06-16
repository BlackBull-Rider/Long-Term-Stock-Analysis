# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Local Data Components Imports
from stocks import SCREENER_WATCHLIST
from core.styles import apply_terminal_theme, render_branding_header, render_terminal_footer
from core.engine import calculate_indian_market_charges, run_massive_scan_engine, scan_ipo_fresh_listings

# ১. থিম ও সিএসএস লাইভ লোড
apply_terminal_theme()
render_branding_header()

# ২. ড্যাশবোর্ড স্টেট প্রিপারেশন
if "portfolio_data_store" not in st.session_state:
    st.session_state.portfolio_data_store = pd.DataFrame(columns=[
        "Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges", 
        "Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"
    ])

master_df = st.session_state.portfolio_data_store
active_portfolio = master_df[master_df["Status"] == "ACTIVE"].reset_index(drop=True)

# ৩. কন্ট্রোল প্যানেল সাইডবার
st.sidebar.title("🦅 Alpha Controls")
st.sidebar.write("`⚡ Operational Safe-Mode: ON`")
st.sidebar.markdown("---")

menu_selection = st.sidebar.radio(
    "TERMINAL NAVIGATION",
    [
        "🔍 Live Screener Core",
        "🚀 Monster Moat Hunt",
        "🚀 IPO Breakout Monitor",
        "📥 Order Desk (Buy/Sell)",
        "📋 Portfolio Tracker Grid",
        "📊 Capital & Risk Analytics"
    ]
)

# =========================================================================
# MODULE RE-ROUTING ENGINE
# =========================================================================

if menu_selection == "🔍 Live Screener Core":
    st.subheader("🦅 High-Speed Batch Institutional Screener")
    st.write("টার্গেট রিটার্নের ওপর ভিত্তি করে সিস্টেম অটোমেটিকলি কোয়ালিটি ফিল্টার রেশিও সেট করবে।")
    st.markdown("---")
    
    st.markdown("#### 🎯 Macro Investment Goals")
    col_g1, col_g2 = st.columns(2)
    invest_horizon = col_g1.number_input("Investment Holding Term (Years)", min_value=0.5, max_value=15.0, value=2.0, step=0.5)
    expected_return = col_g2.number_input("Minimum Target Return Expected (% p.a.)", min_value=10.0, max_value=150.0, value=25.0, step=5.0)
    
    # 🚀 সম্পূর্ণ ডাইনামিক স্ল্যাব লজিক (৫০% থেকে ১৫০% পর্যন্ত আলাদা কড়া ভ্যালু আসবে)
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
    
    st.markdown("#### 📊 Dynamic Fundamental Quality Matrix (Editable)")
    col_f1, col_f2 = st.columns(2)
    min_sales = col_f1.number_input("Min Sales Growth (%)", min_value=0.0, max_value=100.0, value=float(calc_sales), step=1.0)
    min_roe = col_f2.number_input("Min ROE (%)", min_value=0.0, max_value=100.0, value=float(calc_roe), step=1.0)
    
    col_f3, col_f4 = st.columns(2)
    max_pe = col_f3.number_input("Max P/E Ratio (0 for Any)", min_value=0.0, max_value=300.0, value=float(calc_pe), step=1.0)
    min_mcap = col_f4.number_input("Min Market Cap (Cr)", min_value=0.0, max_value=500000.0, value=float(calc_mcap), step=100.0)

    st.markdown("#### 🏢 Institutional Ownership & Tech Setup")
    col_o1, col_o2 = st.columns(2)
    min_promoter = col_o1.number_input("Min Promoter Holding (%)", min_value=0.0, max_value=100.0, value=float(calc_promoter), step=1.0)
    min_ema200_dist = col_o2.number_input("Min Distance from 200 EMA (%)", min_value=-50.0, max_value=100.0, value=float(calc_ema_dist), step=0.5)
    
    st.markdown("---")
    
    if st.button("⚡ EXECUTE COMPLIANT BATCH SCAN", use_container_width=True):
        status_box = st.empty()
        status_box.info("🌪️ Fetching 7-Year History from Safe Cache Replica...")
        
        expanded_watchlist = SCREENER_WATCHLIST * 10
        raw_results = run_massive_scan_engine(expanded_watchlist, invest_horizon, expected_return)
        
        filtered_results = []
        for res in raw_results:
            if not res: continue
            if (res["Sales Growth (%)"] >= min_sales and res["ROE (%)"] >= min_roe and 
                res["Market Cap (Cr)"] >= min_mcap and (max_pe == 0 or res["P/E Ratio"] <= max_pe)):
                
                raw_promoter = res["Promoter (%)"]
                val_promoter = float(raw_promoter) if isinstance(raw_promoter, (int, float)) else 0.0
                actual_ema200_dist = float(res["EMA200 Dist (%)"].replace("%",""))
                
                if val_promoter >= min_promoter and actual_ema200_dist >= min_ema200_dist:
                    filtered_results.append(res)
                    
        status_box.empty()
        if filtered_results:
            st.success(f"🎯 Scan Complete! Found {len(filtered_results)} institutional setups.")
            df_display = pd.DataFrame(filtered_results)
            
            # চার্ট সেটআপ কলামটি ২ নম্বরে পজিশন করা হলো
            final_cols = ["Stock", "Chart Setup", "CMP (₹)", "P/E Ratio", "ROE (%)", "Promoter (%)", "Max DD (%)", "EMA200 Dist (%)", "System Action"]
            st.dataframe(df_display[final_cols], use_container_width=True)

elif menu_selection == "🚀 Monster Moat Hunt":
    st.subheader("🔥 Monster Moat Catalyst Scanner (1000% Multibagger Hunt)")
    st.write("ব্র্যান্ড ভ্যালু, কাস্টমার রিভিউ এবং প্রমোশনের অদৃশ্য শক্তির কোয়ালিটেটিভ স্ক্রেনার।")
    st.markdown("---")
    
    col_m1, col_m2 = st.columns(2)
    min_gross_margin = col_m1.number_input("Minimum Gross Margin % (Brand Premium)", min_value=20.0, max_value=90.0, value=45.0, step=1.0)
    min_inventory_speed = col_m2.number_input("Minimum Inventory Speed (Consumer Demand)", min_value=2.0, max_value=25.0, value=6.0, step=0.5)
    
    if st.button("🚀 EXECUTE 1000% MONSTER MOAT SCAN", use_container_width=True):
        status = st.empty()
        status.warning("🌪️ Compiling 7-Year Chart Setups + Brand Moat Matrix...")
        
        expanded_watchlist = SCREENER_WATCHLIST * 10
        raw_results = run_massive_scan_engine(expanded_watchlist, invest_horizon=2.0, expected_return=50.0)
        
        moat_hits = []
        for res in raw_results:
            if not res: continue
            if res["Gross Margin (%)"] >= min_gross_margin and res["Inventory Speed (x)"] >= min_inventory_speed:
                if res["ROE (%)"] >= 20.0:  # হাই আলফা ফিল্টার
                    moat_hits.append(res)
                    
        status.empty()
        if moat_hits:
            st.success(f"🔥 BOOM! Found {len(moat_hits)} Mega Monopoly Brands.")
            df_moat = pd.DataFrame(moat_hits)
            moat_cols = ["Stock", "Chart Setup", "CMP (₹)", "Gross Margin (%)", "Inventory Speed (x)", "Marketing Efficiency (x)", "ROE (%)", "System Action"]
            st.dataframe(df_moat[moat_cols], use_container_width=True)
        else:
            st.warning("No asset found matching this extreme level of pricing power.")

elif menu_selection == "🚀 IPO Breakout Monitor":
    st.subheader("🚀 Fresh Listings & IPO Breakout Matrix")
    if st.button("🔥 Scan IPO Fresh Liquid Assets", use_container_width=True):
        ipo_hits = scan_ipo_fresh_listings(SCREENER_WATCHLIST[:15])
        if ipo_hits: st.dataframe(pd.DataFrame(ipo_hits), use_container_width=True)
        else: st.info("No active IPO breakout structures identified today.")

elif menu_selection == "📥 Order Desk (Buy/Sell)" or menu_selection == "📋 Portfolio Tracker Grid" or menu_selection == "📊 Capital & Risk Analytics":
    st.subheader("📡 Operational Layer")
    st.info("System is running in safe read-only screener mode. Open port to activate transactions.")

render_terminal_footer()
