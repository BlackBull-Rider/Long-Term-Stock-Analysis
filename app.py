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

# ==========================
# INIT
# ==========================

create_tables()

st.set_page_config(
    page_title="Green Bull Rider V6",
    page_icon="🦅",
    layout="wide"
)

# ==========================
# HEADER
# ==========================

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

        with st.spinner(
            "Scanning Stocks..."
        ):

            completed = run_scan(limit)

        st.success(
            f"{completed} Stocks Scanned Successfully"
        )

# ==========================
# PORTFOLIO
# ==========================

elif menu == "Portfolio":

    st.header("💼 Portfolio")

    stock_options = get_stock_options()

    tab1, tab2, tab3 = st.tabs(
        [
            "Buy",
            "Sell",
            "Holdings"
        ]
    )

    # ==========================
    # BUY
    # ==========================

    with tab1:

        st.subheader("Buy Stock")

        selected_stock = st.selectbox(
            "Search Stock",
            stock_options,
            index=None,
            placeholder="Type RELIANCE, TCS, INFY..."
        )

        qty = st.number_input(
            "Quantity",
            min_value=1.0,
            value=1.0,
            key="buy_qty"
        )

        price = st.number_input(
            "Buy Price",
            min_value=0.0,
            value=0.0,
            key="buy_price"
        )

        if st.button("✅ Buy"):

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

                st.success(
                    f"{symbol} Added Successfully"
                )

    # ==========================
    # SELL
    # ==========================

    with tab2:

        st.subheader("Sell Stock")

        selected_stock = st.selectbox(
            "Select Stock To Sell",
            stock_options,
            index=None,
            key="sell_symbol"
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

        if st.button("❌ Sell"):

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

                st.success(
                    f"{symbol} Sold Successfully"
                )

    # ==========================
    # HOLDINGS
    # ==========================

    with tab3:

        st.subheader(
            "Current Holdings"
        )

        holdings = get_portfolio()

        st.dataframe(
            holdings,
            use_container_width=True
        )

        st.subheader(
            "Transaction History"
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

    st.subheader(
        f"Found {len(df)} Stocks"
    )

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning(
            "No Stocks Found"
        )

# ==========================
# IPO SCANNER
# ==========================

elif menu == "IPO Scanner":

    st.header("🆕 IPO Discovery")

    st.info(
        "IPO Module Coming Soon"
    )
