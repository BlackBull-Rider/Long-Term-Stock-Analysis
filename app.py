# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# ৫০০টি স্টকের মূল লিস্ট লোড
from stocks import SCREENER_WATCHLIST

# [🔗 কানেকশন লেয়ার]: core ফোল্ডার থেকে আলাদা করা ডিজাইন ও ব্যাকএন্ড ইঞ্জিন ইম্পোর্ট
from core.styles import apply_terminal_theme, render_branding_header, render_terminal_footer
from core.engine import calculate_indian_market_charges, analyze_stock_advanced

# ১. সিস্টেম থিম অ্যাপ্লাই করা হলো (UI Layer Link)
apply_terminal_theme()

# ২. ব্র্যান্ডিং হেডার রেন্ডার (UI Layer Link)
render_branding_header()

# ৩. ইন্টারনাল সেশন ডাটাবেস হ্যান্ডলার
if "portfolio_data_store" not in st.session_state:
    st.session_state.portfolio_data_store = pd.DataFrame(columns=[
        "Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges", 
        "Sell Price", "Sell Date", "Sell Charges", "Realized P&L", "Status"
    ])

master_df = st.session_state.portfolio_data_store
active_portfolio = master_df[master_df["Status"] == "ACTIVE"].reset_index(drop=True)
closed_portfolio = master_df[master_df["Status"] == "CLOSED"].reset_index(drop=True)

# ৪. সাইডবার নেভিগেশন ও ফান্ড ম্যানেজার উইজডম কোটস
st.sidebar.title("🦅 Alpha Controls")
st.sidebar.write("`⚡ Modular Architecture v4.0`")
st.sidebar.markdown("---")

menu_selection = st.sidebar.radio(
    "TERMINAL NAVIGATION",
    [
        "🔍 Live Screener Core",
        "📥 Order Desk (Buy/Sell)",
        "📋 Portfolio Tracker Grid",
        "📊 Capital & Risk Analytics",
        "📜 Closed Ledger History"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Fund Manager Wisdom")
quotes = [
    "“The goal of a successful trader is to make the best trades. Money is secondary.” — Alexander Elder",
    "“Rely on liquidity sweeps and dynamic EMAs, not on retail emotions.”",
    "“Amateurs think about how much money they can make. Professionals think about how much they could lose.”"
]
st.sidebar.warning(random.choice(quotes))

# =========================================================================
# 🗺️ CONTROLLER ROUTING ENGINE (মেনু অনুযায়ী পেজ এবং লাইভ ডেটা ম্যাপার)
# =========================================================================

# --- পেজ ১: লাইভ স্ক্রেনার ---
if menu_selection == "🔍 Live Screener Core":
    st.subheader("🦅 Factor Flow Screener System")
    min_sales = st.slider("Min Sales Growth (%)", 0.0, 100.0, 15.0)
    min_roe = st.slider("Min ROE (%)", 0.0, 100.0, 15.0)
    
    col_s1, col_s2 = st.columns(2)
    max_pe = col_s1.number_input("Max P/E Ratio", 0.0, 200.0, 40.0)
    min_mcap = col_s2.number_input("Min Market Cap (Cr)", 0.0, 10000.0, 500.0)
    
    if st.button("🔥 Run Institutional Scan", use_container_width=True):
        progress = st.progress(0)
        results = []
        for index, ticker in enumerate(SCREENER_WATCHLIST[:20]):
            progress.progress((index + 1) / 20)
            res = analyze_stock_advanced(ticker) # ইঞ্জিন কল
            if res:
                if res["Sales Growth (%)"] >= min_sales and res["ROE (%)"] >= min_roe and res["Market Cap (Cr)"] >= min_mcap and (max_pe == 0 or res["P/E Ratio"] <= max_pe):
                    results.append(res)
        progress.empty()
        if results:
            st.dataframe(pd.DataFrame(results)[["Stock", "CMP (₹)", "P/E Ratio", "ROE (%)", "System Action"]], use_container_width=True)

# --- পেজ ২: অর্ডার এক্সিকিউশন প্যানেল ---
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
                b_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=True) # ইঞ্জিন কল
                if stock_name in master_df[(master_df['Stock'] == stock_name) & (master_df['Status'] == 'ACTIVE')]['Stock'].values:
                    idx = master_df[(master_df['Stock'] == stock_name) & (master_df['Status'] == 'ACTIVE')].index[0]
                    master_df.loc[idx, ['Buy Price', 'Quantity', 'Buy Date', 'Buy Charges']] = [
                        ((float(master_df.loc[idx, 'Buy Price']) * int(master_df.loc[idx, 'Quantity'])) + (input_price * input_qty)) / (int(master_df.loc[idx, 'Quantity']) + input_qty),
                        int(master_df.loc[idx, 'Quantity']) + input_qty, str(trade_date), float(master_df.loc[idx, 'Buy Charges']) + b_charges
                    ]
                else:
                    new_row = pd.DataFrame([{"Stock": stock_name, "Buy Price": input_price, "Quantity": input_qty, "Buy Date": str(trade_date), "Buy Charges": b_charges, "Sell Price": 0.0, "Sell Date": "-", "Sell Charges": 0.0, "Realized P&L": 0.0, "Status": "ACTIVE"}])
                    master_df = pd.concat([master_df, new_row], ignore_index=True)
                st.session_state.portfolio_data_store = master_df
                st.success(f"⚡ Order Logged! Taxes: ₹{b_charges}")
                st.rerun()
            else:
                idx = master_df[(master_df['Stock'] == stock_name) & (master_df['Status'] == 'ACTIVE')].index[0]
                old_qty = int(master_df.loc[idx, 'Quantity'])
                buy_p = float(master_df.loc[idx, 'Buy Price'])
                b_date = master_df.loc[idx, 'Buy Date']
                b_charges = float(master_df.loc[idx, 'Buy Charges'])
                
                s_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=False) # ইঞ্জিন কল
                allocated_buy_charge = b_charges * (input_qty / old_qty)
                realized_pnl = ((input_price - buy_p) * input_qty) - (allocated_buy_charge + s_charges)
                
                if input_qty >= old_qty:
                    master_df.loc[idx, ['Sell Price', 'Sell Date', 'Sell Charges', 'Realized P&L', 'Status']] = [input_price, str(trade_date), s_charges, realized_pnl, "CLOSED"]
                else:
                    master_df.loc[idx, 'Quantity'] = old_qty - input_qty
                    master_df.loc[idx, 'Buy Charges'] = b_charges - allocated_buy_charge
                    partial_closed_row = pd.DataFrame([{"Stock": stock_name, "Buy Price": buy_p, "Quantity": input_qty, "Buy Date": b_date, "Buy Charges": allocated_buy_charge, "Sell Price": input_price, "Sell Date": str(trade_date), "Sell Charges": s_charges, "Realized P&L": realized_pnl, "Status": "CLOSED"}])
                    master_df = pd.concat([master_df, partial_closed_row], ignore_index=True)
                st.session_state.portfolio_data_store = master_df
                st.success(f"🚨 Position Liquidated! Sell Tax: ₹{s_charges}")
                st.rerun()

# --- পেজ ৩: পোর্টফোলিও ট্র্যাকার গ্রিড ---
elif menu_selection == "📋 Portfolio Tracker Grid":
    st.subheader("📋 Core Running Positions")
    if active_portfolio.empty:
        st.info("💡 Portfolio Core empty. Open Order Desk to execute entries.")
    else:
        with st.spinner("Processing Terminal Data..."):
            port_results = [analyze_stock_advanced(row["Stock"], float(row["Buy Price"]), int(row["Quantity"]), float(row["Buy Charges"])) for _, row in active_portfolio.iterrows()]
            port_results = [r for r in port_results if r]
            if port_results:
                st.dataframe(pd.DataFrame(port_results)[["Stock", "Qty", "Avg Buy (₹)", "CMP (₹)", "Invested (₹)", "Current Value (₹)", "Net P&L (₹)", "Net Return (%)", "System Action"]], use_container_width=True)

# --- পেজ ৪: ক্যাপিটাল অ্যান্ড রিস্ক অ্যানালিসিস ড্যাশবোর্ড ---
elif menu_selection == "📊 Capital & Risk Analytics":
    st.subheader("📊 Quant Asset Risk Dashboard")
    if active_portfolio.empty:
        st.info("💡 Analytics Engine offline due to zero active positions.")
    else:
        with st.spinner("Running Beta Matrix Algorithms..."):
            port_results = [analyze_stock_advanced(row["Stock"], float(row["Buy Price"]), int(row["Quantity"]), float(row["Buy Charges"])) for _, row in active_portfolio.iterrows()]
            port_results = [r for r in port_results if r]
            if port_results:
                port_df = pd.DataFrame(port_results)
                t_invested, t_current, t_pnl = port_df["Invested (₹)"].sum(), port_df["Current Value (₹)"].sum(), port_df["Net P&L (₹)"].sum()
                weighted_beta = (port_df["Beta"] * (port_df["Current Value (₹)"] / t_current)).sum()
                
                st.metric("Total Invested Capital (Post-Tax Cost)", f"₹{t_invested:,.2f}")
                st.metric("Net Liquid Floating Value", f"₹{t_current:,.2f}")
                st.metric("Pure Alpha Strategy Net P&L", f"₹{t_pnl:,.2f}", f"{(t_pnl/t_invested)*100:.2f}%")
                st.metric("System Volatility Coefficient (Beta)", f"{weighted_beta:.2f}")
                
                st.markdown("---")
                st.plotly_chart(px.pie(port_df, values="Current Value (₹)", names="Stock", hole=0.4, color_discrete_sequence=px.colors.sequential.Tealgrn), use_container_width=True)
                st.plotly_chart(px.bar(port_df, x="Stock", y="Max DD (%)", color="Max DD (%)", color_continuous_scale="Reds_r"), use_container_width=True)

# --- পেজ ৫: ক্লোজড ট্রেইড হিস্ট্রি লেজার ---
elif menu_selection == "📜 Closed Ledger History":
    st.subheader("📜 Realized Alpha Vault Ledger")
    if closed_portfolio.empty:
        st.info("💡 Closed history database clean.")
    else:
        st.metric("Net Closed Profit (Post-Tax Pure Cash)", f"₹{closed_portfolio['Realized P&L'].sum():,.2f}")
        st.dataframe(closed_portfolio[["Stock", "Quantity", "Buy Price", "Buy Charges", "Sell Price", "Sell Charges", "Realized P&L"]], use_container_width=True)

# ৫. প্রফেশনাল ব্রোকার ফুটার রেন্ডার (UI Layer Link)
render_terminal_footer()
