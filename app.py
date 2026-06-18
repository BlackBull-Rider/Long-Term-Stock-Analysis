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
    get_transactions
)

create_tables()

st.set_page_config(
    page_title="Green Bull Rider V6",
    page_icon="🦅",
    layout="wide"
)

st.title("🦅 Green Bull Rider V6")

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

if menu == "Dashboard":

    st.header("📊 Dashboard")
    st.success("System Ready")

elif menu == "Universe Loader":

    st.header("📥 NSE Universe Loader")

    if st.button("🚀 Load NSE Universe"):

        total = load_nse_universe()

        st.success(
            f"{total} Stocks Loaded"
        )

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

elif menu == "Portfolio":

    st.header("💼 Portfolio")

    tab1, tab2, tab3 = st.tabs(
        ["Buy", "Sell", "Holdings"]
    )

    with tab1:

        symbol = st.text_input(
            "Symbol"
        ).upper()

        qty = st.number_input(
            "Quantity",
            min_value=1.0
        )

        price = st.number_input(
            "Price",
            min_value=0.0
        )

        if st.button("Buy Stock"):

            buy_stock(
                symbol,
                qty,
                price
            )

            st.success(
                "Stock Added"
            )

    with tab2:

        symbol = st.text_input(
            "Sell Symbol"
        ).upper()

        qty = st.number_input(
            "Sell Quantity",
            min_value=1.0
        )

        price = st.number_input(
            "Sell Price",
            min_value=0.0
        )

        if st.button("Sell Stock"):

            sell_stock(
                symbol,
                qty,
                price
            )

            st.success(
                "Stock Sold"
            )

    with tab3:

        holdings = get_portfolio()

        st.subheader(
            "Holdings"
        )

        st.dataframe(
            holdings,
            use_container_width=True
        )

        txns = get_transactions()

        st.subheader(
            "Transactions"
        )

        st.dataframe(
            txns,
            use_container_width=True
        )

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

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

elif menu == "IPO Scanner":

    st.header("🆕 IPO Discovery")

    st.info(
        "Coming Soon"
    )
