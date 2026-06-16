# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# stocks Watchlist load
from stocks import SCREENER_WATCHLIST

# [🔗 কানেকশন লেয়ার]
from core.styles import apply_terminal_theme, render_branding_header, render_terminal_footer
from core.engine import calculate_indian_market_charges, analyze_stock_advanced, run_massive_scan_engine, scan_ipo_fresh_listings

# ১. থিম ও হেডার অ্যাপ্লাই
apply_terminal_theme()
render_branding_header()

# ২. ইন্টারনাল সেশন ডাটাবেস
if "portfolio_data_store" not in st.session_state:
    st.session_state.portfolio_data_store = pd.DataFrame(columns=[
        "Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges", 
        "Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"
    ])

master_df = st.session_state.portfolio_data_store
active_portfolio = master_df[master_df["Status"] == "ACTIVE"].reset_index(drop=True)
closed_portfolio = master_df[master_df["Status"] == "CLOSED"].reset_index(drop=True)

# ৩. সাইডবার নেভিগেশন
st.sidebar.title("🦅 Alpha Controls")
st.sidebar.write("`⚡ Institutional Master v8.0`")
st.sidebar.markdown("---")

menu_selection = st.sidebar.radio(
    "TERMINAL NAVIGATION",
    [
        "🔍 Live Screener Core",
        "🚀 IPO Breakout Monitor",
        "📥 Order Desk (Buy/Sell)",
        "📋 Portfolio Tracker Grid",
        "📊 Capital & Risk Analytics",
        "📜 Closed Ledger History"
    ]
)

# =========================================================================
# 🗺️ CONTROLLER ROUTING ENGINE
# =========================================================================

if menu_selection == "🔍 Live Screener Core":
    st.subheader("🦅 Dynamic Fair-Value Institutional Screener")
    st.write("Holding Term এবং Return গোল দিন; অ্যালগরিদম অটোমেটিক বক্সে ফেয়ার প্যারামিটার বসিয়ে দেবে।")
    st.markdown("---")
    
    # 🎯 সেকশন ১: সবার ওপরে প্রাইমারী গোল ইনপুট
    st.markdown("#### 🎯 Macro Investment Goals")
    col_g1, col_g2 = st.columns(2)
    invest_horizon = col_g1.number_input("Investment Holding Term (Years)", min_value=0.5, max_value=15.0, value=2.0, step=0.5)
    expected_return = col_g2.number_input("Minimum Target Return Expected (% p.a.)", min_value=10.0, max_value=150.0, value=25.0, step=5.0)
    
    # 🧠 ব্যাকঅ্যান্ড ফেয়ার-ভ্যালু গাণিতিক ম্যাট্রিক্স
    if expected_return >= 40:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 18.0, 22.0, 35.0, 2.0
    elif expected_return >= 25:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 12.0, 15.0, 50.0, 1.0
    else:
        calc_sales, calc_roe, calc_pe, calc_ema_dist = 10.0, 12.0, 65.0, 0.0

    calc_mcap = 1500.0 if invest_horizon <= 1.0 else 1000.0
    calc_promoter = 40.0 if expected_return > 35 else 30.0
    
    # 📊 সেকশন ২: অটো-ক্যালকুলেটেড প্যারামিটার (ইউজার এডিটেবল)
    st.markdown("#### 📊 Dynamic Fundamental Quality Matrix (Editable)")
    col_f1, col_f2 = st.columns(2)
    min_sales = col_f1.number_input("Min Sales Growth (%)", min_value=0.0, max_value=100.0, value=float(calc_sales), step=1.0)
    min_roe = col_f2.number_input("Min ROE (%)", min_value=0.0, max_value=100.0, value=float(calc_roe), step=1.0)
    
    col_f3, col_f4 = st.columns(2)
    max_pe = col_f3.number_input("Max P/E Ratio (0 for Any)", min_value=0.0, max_value=300.0, value=float(calc_pe), step=1.0)
    min_mcap = col_f4.number_input("Min Market Cap (Cr)", min_value=0.0, max_value=500000.0, value=float(calc_mcap), step=100.0)

    st.markdown("#### 🏢 Institutional Ownership & Tech Setup (Editable)")
    col_o1, col_o2 = st.columns(2)
    min_promoter = col_o1.number_input("Min Promoter Holding (%)", min_value=0.0, max_value=100.0, value=float(calc_promoter), step=1.0)
    min_ema200_dist = col_o2.number_input("Min Distance from 200 EMA (%)", min_value=-50.0, max_value=100.0, value=float(calc_ema_dist), step=0.5)
    
    require_golden_cross = st.selectbox("Trend Momentum (50 EMA > 200 EMA)", ["REQUIRED (Bullish Structure)", "ANY STRUCTURE"], index=0)
    
    st.markdown("---")
    
    if st.button("⚡ EXECUTE FLASH BATCH STORM SCAN (3 SEC)", use_container_width=True):
        status_box = st.empty()
        status_box.info("🌪️ Fetching Packets from Exchange via Bulk Batch Tunnel...")
        
        expanded_watchlist = SCREENER_WATCHLIST * 10  # ৫০০০ স্টক সিমুলেশন
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
            st.success(f"🎯 Complete! Found {len(filtered_results)} setups in RAM Database.")
            df_display = pd.DataFrame(filtered_results)
            final_cols = ["Stock", "CMP (₹)", "P/E Ratio", "ROE (%)", "Promoter (%)", "Institutions (%)", "Dividend (%)", "EMA200 Dist (%)", "System Action"]
            st.dataframe(df_display[final_cols], use_container_width=True)
        else:
            st.warning("No assets matched your exact config.")

elif menu_selection == "🚀 IPO Breakout Monitor":
    st.subheader("🚀 Fresh Listings & IPO Breakout Matrix")
    st.write("যেসব নতুন স্টক গত কয়েক মাস বা কয়েক দিনে লিস্ট হয়েছে এবং বড় প্লেয়াররা সেখানে এন্ট্রি নিচ্ছে।")
    st.markdown("---")
    
    if st.button("🔥 Scan IPO Fresh Liquid Assets", use_container_width=True):
        status = st.empty()
        status.info("🔍 Scanning recent IPO brackets for Volume Surges...")
        
        # আইপিও ওয়াচলিস্ট লোড (ওয়াচলিস্টের শর্ট টিকার টেস্ট করার জন্য)
        ipo_hits = scan_ipo_fresh_listings(SCREENER_WATCHLIST[:15])
        status.empty()
        
        if ipo_hits:
            st.success(f"⚡ High-Alpha IPO Formations Identified!")
            st.dataframe(pd.DataFrame(ipo_hits), use_container_width=True)
        else:
            st.info("No fresh listing is currently offering an institutional volume spike breakout.")

elif menu_selection == "📥 Order Desk (Buy/Sell)":
    st.subheader("⚡ High-Speed Execution Matrix")
    trade_type = st.radio("Execute Type:", ["🛒 BUY (Add / Top-up)", "💰 SELL (Reduce/Exit)"], horizontal=True)
    with st.form("portfolio_form", clear_on_submit=True):
        if "BUY" in trade_type:
            stock_name = st.selectbox("Select Asset to ACCUMULATE", options=sorted(SCREENER_WATCHLIST), index=None)
            input_price = st.number_input("Price (₹)", min_value=0.1, step=0.1)
            input_qty = st.number_input("Volume/Qty", min_value=1, step=1)
            trade_date = st.date_input("Date", datetime.now())
        else:
            stock_name = st.selectbox("Select Asset to LIQUIDATE", options=sorted(active_portfolio["Stock"].unique()) if not active_portfolio.empty else ["No Holding"], index=None)
            input_price = st.number_input("Price (₹)", min_value=0.1, step=0.1)
            input_qty = st.number_input("Volume/Qty", min_value=1, step=1)
            trade_date = st.date_input("Date", datetime.now())
            
        if st.form_submit_button("🔥 Fire Transaction", use_container_width=True) and stock_name and stock_name != "No Holding":
            if "BUY" in trade_type:
                b_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=True)
                clean_name = stock_name.split(" [")[0] if " [" in stock_name else stock_name
                if clean_name in master_df[(master_df['Status'] == 'ACTIVE')]['Stock'].values:
                    idx = master_df[(master_df['Stock'] == clean_name) & (master_df['Status'] == 'ACTIVE')].index[0]
                    master_df.loc[idx, ['Buy Price', 'Quantity', 'Buy Date', 'Buy Charges']] = [
                        ((float(master_df.loc[idx, 'Buy Price']) * int(master_df.loc[idx, 'Quantity'])) + (input_price * input_qty)) / (int(master_df.loc[idx, 'Quantity']) + input_qty),
                        int(master_df.loc[idx, 'Quantity']) + input_qty, str(trade_date), float(master_df.loc[idx, 'Buy Charges']) + b_charges
                    ]
                else:
                    new_row = pd.DataFrame([{"Stock": clean_name, "Buy Price": input_price, "Quantity": input_qty, "Buy Date": str(trade_date), "Buy Charges": b_charges, "Sell Price": 0.0, "Sell Date": "-", "Sell Charges": 0.0, "Realized P&L": 0.0, "Status": "ACTIVE"}])
                    master_df = pd.concat([master_df, new_row], ignore_index=True)
                st.session_state.portfolio_data_store = master_df
                st.success(f"⚡ Order Logged! Taxes: ₹{b_charges}")
                st.rerun()

elif menu_selection == "📋 Portfolio Tracker Grid":
    st.subheader("📋 Core Running Positions")
    if active_portfolio.empty: st.info("💡 Portfolio vacant.")
    else:
        with st.spinner("Processing..."):
            port_results = [analyze_stock_advanced(row["Stock"], float(row["Buy Price"]), int(row["Quantity"]), float(row["Buy Charges"])) for _, row in active_portfolio.iterrows()]
            st.dataframe(pd.DataFrame([p for p in port_results if p])[["Stock", "Qty", "Avg Buy (₹)", "CMP (₹)", "Invested (₹)", "Current Value (₹)", "Net P&L (₹)", "Net Return (%)"]], use_container_width=True)

elif menu_selection == "📊 Capital & Risk Analytics":
    st.subheader("📊 Quant Asset Risk Dashboard")
    if active_portfolio.empty: st.info("💡 Analytics Offline.")
    else:
        port_results = [analyze_stock_advanced(row["Stock"], float(row["Buy Price"]), int(row["Quantity"]), float(row["Buy Charges"])) for _, row in active_portfolio.iterrows()]
        port_df = pd.DataFrame([p for p in port_results if p])
        st.metric("Total Deployed Capital", f"₹{port_df['Invested (₹)'].sum():,.2f}")
        st.plotly_chart(px.pie(port_df, values="Current Value (₹)", names="Raw_Stock", hole=0.4, color_discrete_sequence=px.colors.sequential.Tealgrn), use_container_width=True)

elif menu_selection == "📜 Closed Ledger History":
    st.subheader("📜 Realized Alpha Vault Ledger")
    st.markdown("### 📥 Export & Data Access Portal")
    col_d1, col_d2 = st.columns(2)
    if not active_portfolio.empty:
        active_csv = active_portfolio[["Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges"]].to_csv(index=False).encode('utf-8')
        col_d1.download_button(label="📥 Download Active Positions (CSV)", data=active_csv, file_name=f"active_portfolio_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
    if not closed_portfolio.empty:
        closed_csv = closed_portfolio[["Stock", "Quantity", "Buy Price", "Buy Charges", "Sell Price", "Sell Charges", "Realized P&L"]].to_csv(index=False).encode('utf-8')
        col_d2.download_button(label="📥 Download Closed Ledger History (CSV)", data=closed_csv, file_name=f"closed_ledger_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
    st.markdown("---")
    if closed_portfolio.empty: st.info("💡 History clean.")
    else: st.dataframe(closed_portfolio[["Stock", "Quantity", "Buy Price", "Realized P&L"]], use_container_width=True)

render_terminal_footer()
