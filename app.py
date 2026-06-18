import streamlit as st

from database.schema import create_tables
from data.load_universe import load_nse_universe
from data.sync_engine import run_scan

from core.screener import (
    breakout_candidates,
    strong_uptrend,
    near_52w_high
)

from core.portfolio import (
    buy_stock,
    sell_stock,
    get_portfolio,
    get_transactions,
    get_stock_options
)

from core.portfolio_summary import (
    portfolio_summary
)

# ==========================
# INIT
# ==========================

create_tables()

st.set_page_config(
    page_title="Green Bull Rider V6",
    page_icon="🦅",
    layout="wide"
)

st.title("🦅 Green Bull Rider V6")

# ==========================
# SIDEBAR
# ==========================

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Universe Loader",
        "Market Scanner",
        "Portfolio",
        "Screener",
        "IPO Scanner"
    ]
)

# ==========================
# DASHBOARD
# ==========================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    st.success("System Ready")

# ==========================
# UNIVERSE LOADER
# ==========================

elif menu == "Universe Loader":

    st.header("📥 NSE Universe Loader")

    if st.button("🚀 Load NSE Universe"):

        total = load_nse_universe()

        st.success(
            f"{total} Stocks Loaded"
        )

# ==========================
# MARKET SCANNER
# ==========================

elif menu == "Market Scanner":

    st.header("📡 Market Scanner")

    limit = st.slider(
        "Stocks To Scan",
        10,
        500,
        50
    )

    if st.button("🚀 Run Scan"):

        completed = run_scan(limit)

        st.success(
            f"{completed} Stocks Scanned"
        )

# ==========================
# PORTFOLIO
# ==========================

elif menu == "Portfolio":

    st.header("💼 Portfolio")

    holdings = get_portfolio()

    summary = portfolio_summary(
        holdings
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Invested",
        f"₹{summary['invested']:,.0f}"
    )

    c2.metric(
        "Current Value",
        f"₹{summary['current']:,.0f}"
    )

    c3.metric(
        "Profit / Loss",
        f"₹{summary['pnl']:,.0f}"
    )

    c4.metric(
        "Return %",
        f"{summary['return_pct']}%"
    )

    st.divider()

    stock_options = get_stock_options()

    tab1, tab2, tab3 = st.tabs(
        [
            "Buy",
            "Sell",
            "Holdings"
        ]
    )

    # BUY

    with tab1:

        selected_stock = st.selectbox(
            "Search Stock",
            stock_options,
            index=None,
            placeholder="Type RELIANCE, TCS..."
        )

        qty = st.number_input(
            "Quantity",
            min_value=1.0,
            value=1.0
        )

        price = st.number_input(
            "Buy Price",
            min_value=0.0,
            value=0.0
        )

        if st.button("Buy Stock"):

            if selected_stock:

                symbol = (
                    selected_stock
                    .split(" - ")[0]
                )

                buy_stock(
                    symbol,
                    qty,
                    price
                )

                st.rerun()

    # SELL

    with tab2:

        selected_stock = st.selectbox(
            "Select Stock",
            stock_options,
            index=None,
            key="sell"
        )

        qty = st.number_input(
            "Sell Quantity",
            min_value=1.0,
            value=1.0,
            key="sell_qty"
        )

        price = st.number_input(
            "Sell Price",
            min_value=0.0,
            value=0.0,
            key="sell_price"
        )

        if st.button("Sell Stock"):

            if selected_stock:

                symbol = (
                    selected_stock
                    .split(" - ")[0]
                )

                sell_stock(
                    symbol,
                    qty,
                    price
                )

                st.rerun()

    # HOLDINGS

    with tab3:

        st.subheader(
            "Current Holdings"
        )

        st.dataframe(
            holdings,
            use_container_width=True
        )

        st.subheader(
            "Transactions"
        )

        txns = get_transactions()

        st.dataframe(
            txns,
            use_container_width=True
        )

# ==========================
# SCREENER
# ==========================

elif menu == "Screener":

    st.header("🔍 Smart Screener")

    screen_type = st.selectbox(
        "Select Screener",
        [
            "Breakout Candidates",
            "Strong Uptrend",
            "Near 52W High"
        ]
    )

    if screen_type == "Breakout Candidates":

        df = breakout_candidates()

    elif screen_type == "Strong Uptrend":

        df = strong_uptrend()

    else:

        df = near_52w_high()

    st.write(
        f"Found {len(df)} Stocks"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

# ==========================
# IPO
# ==========================

elif menu == "IPO Scanner":

    st.header("🆕 IPO Discovery")

    st.info(
        "Coming Soon"
    )
