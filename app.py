# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# estate/stocks Watchlist load
from stocks import SCREENER_WATCHLIST

# [🔗 কানেকশন লেয়ার]
from core.styles import apply_terminal_theme, render_branding_header, render_terminal_footer
from core.engine import calculate_indian_market_charges, analyze_stock_advanced

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
st.sidebar.write("`⚡ Institutional Core v5.0`")
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
    "“FIIs and Promoters dictate the macro direction; retail volume just fills the gaps.”",
    "“Fundamentals tell you WHAT to buy. Technicals tell you WHEN to buy.”",
    "“Amateurs think about how much money they can make. Professionals think about how much they could lose.”"
]
st.sidebar.warning(random.choice(quotes))

# =========================================================================
# 🗺️ CONTROLLER ROUTING ENGINE
# =========================================================================

if menu_selection == "🔍 Live Screener Core":
    st.subheader("🦅 Alpha Valuation & Ownership Screener")
    st.write("কোম্পানির শেয়ারহোল্ডিং প্যাটার্ন, ডিভিডেন্ড এবং টাইম-হরাইজন ভিত্তিক ভ্যালুয়েশন ট্র্যাকিং ককপিট।")
    st.markdown("---")
    
    # --- আল্ট্রা-ক্লিন ইউজার গোল ফিল্টার (বাকি প্যারামিটার ব্যাকঅ্যান্ডে অটো-লকড) ---
    col_g1, col_g2 = st.columns(2)
    invest_horizon = col_g1.number_input("Investment Holding Term (Years)", min_value=0.5, max_value=15.0, value=2.0, step=0.5)
    expected_return = col_g2.number_input("Minimum Target Return Expected (% p.a.)", min_value=10.0, max_value=150.0, value=25.0, step=5.0)
    
    if st.button("🔥 Run Advanced Valuation Scan", use_container_width=True):
        progress = st.progress(0)
        results = []
        
        # প্রজেক্টের প্রথম ২০টি ওয়াচলিস্ট স্টক লাইভ স্ক্যান করা হচ্ছে
        for index, ticker in enumerate(SCREENER_WATCHLIST[:20]):
            progress.progress((index + 1) / 20)
            
            # ব্যাকঅ্যান্ড ইঞ্জিনে ডাইনামিক প্যারামিটার পাস
            res = analyze_stock_advanced(
                ticker, 
                invest_horizon=invest_horizon, 
                expected_return=expected_return
            )
            
            if res:
                # প্রফেশনাল প্রাতিষ্ঠানিক ফিল্টারিং ফিল্টার (ইন-বিল্ট লকড প্রোটোকল)
                # কোম্পানিকে অবশ্যই ১০০০ কোটির ওপরে মার্কেট ক্যাপ এবং ১০% এর বেশি ROE হোল্ড করতে হবে
                if res["Market Cap (Cr)"] >= 1000 and res["ROE (%)"] >= 10:
                    results.append(res)
                    
        progress.empty()
        
        if results:
            st.success(f"🎯 Analysis Completed! Found {len(results)} high-grade structures.")
            df_display = pd.DataFrame(results)
            
            # প্রফেশনাল কলাম ডিসপ্লে অর্ডারিং
            final_cols = [
                "Stock", "CMP (₹)", "P/E Ratio", "ROE (%)", "Promoter (%)", 
                "Institutions (%)", "Dividend (%)", "EMA200 Dist (%)", "System Action"
            ]
            st.dataframe(df_display[final_cols], use_container_width=True)
        else:
            st.warning("No institutional grade assets matched your criteria. Consider decreasing expected returns.")

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
                # স্টক নেম ম্যাচ করার জন্য টেক্সট ক্লিন স্প্লিট লজিক
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
            else:
                clean_name = stock_name.split(" [")[0] if " [" in stock_name else stock_name
                idx = master_df[(master_df['Stock'] == clean_name) & (master_df['Status'] == 'ACTIVE')].index[0]
                old_qty = int(master_df.loc[idx, 'Quantity'])
                buy_p = float(master_df.loc[idx, 'Buy Price'])
                b_date = master_df.loc[idx, 'Buy Date']
                b_charges = float(master_df.loc[idx, 'Buy Charges'])
                
                s_charges = calculate_indian_market_charges(input_price, input_qty, is_buy=False)
                allocated_buy_charge = b_charges * (input_qty / old_qty)
                realized_pnl = ((input_price - buy_p) * input_qty) - (allocated_buy_charge + s_charges)
                
                if input_qty >= old_qty:
                    master_df.loc[idx, ['Sell Price', 'Sell Date', 'Sell Charges', 'Realized P&L', 'Status']] = [input_price, str(trade_date), s_charges, realized_pnl, "CLOSED"]
                else:
                    master_df.loc[idx, 'Quantity'] = old_qty - input_qty
                    master_df.loc[idx, 'Buy Charges'] = b_charges - allocated_buy_charge
                    partial_closed_row = pd.DataFrame([{"Stock": clean_name, "Buy Price": buy_p, "Quantity": input_qty, "Buy Date": b_date, "Buy Charges": allocated_buy_charge, "Sell Price": input_price, "Sell Date": str(trade_date), "Sell Charges": s_charges, "Realized P&L": realized_pnl, "Status": "CLOSED"}])
                    master_df = pd.concat([master_df, partial_closed_row], ignore_index=True)
                st.session_state.portfolio_data_store = master_df
                st.success(f"🚨 Position Liquidated! Sell Tax: ₹{s_charges}")
                st.rerun()

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
                st.plotly_chart(px.pie(port_df, values="Current Value (₹)", names="Raw_Stock", hole=0.4, color_discrete_sequence=px.colors.sequential.Tealgrn), use_container_width=True)
                st.plotly_chart(px.bar(port_df, x="Raw_Stock", y="Max DD (%)", color="Max DD (%)", color_continuous_scale="Reds_r"), use_container_width=True)

elif menu_selection == "📜 Closed Ledger History":
    st.subheader("📜 Realized Alpha Vault Ledger")
    st.markdown("### 📥 Export & Data Access Portal")
    col_d1, col_d2 = st.columns(2)
    
    if not active_portfolio.empty:
        active_csv = active_portfolio[["Stock", "Buy Price", "Quantity", "Buy Date", "Buy Charges"]].to_csv(index=False).encode('utf-8')
        col_d1.download_button(label="📥 Download Active Positions (CSV)", data=active_csv, file_name=f"active_portfolio_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
    else:
        col_d1.info("No active positions to export.")
        
    if not closed_portfolio.empty:
        closed_csv = closed_portfolio[["Stock", "Quantity", "Buy Price", "Buy Charges", "Sell Price", "Sell Charges", "Realized P&L"]].to_csv(index=False).encode('utf-8')
        col_d2.download_button(label="📥 Download Closed Ledger History (CSV)", data=closed_csv, file_name=f"closed_ledger_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
    else:
        col_d2.info("No closed history to export.")
        
    st.markdown("---")
    if closed_portfolio.empty:
        st.info("💡 Closed history database clean.")
    else:
        st.metric("Net Closed Profit (Post-Tax Pure Cash)", f"₹{closed_portfolio['Realized P&L'].sum():,.2f}")
        st.dataframe(closed_portfolio[["Stock", "Quantity", "Buy Price", "Buy Charges", "Sell Price", "Sell Charges", "Realized P&L"]], use_container_width=True)

# ফুটার রেন্ডার
render_terminal_footer()
