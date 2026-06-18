import streamlit as st

from database.schema import create_tables
from data.load_universe import load_nse_universe
from data.sync_engine import run_scan
from core.screener import (
    breakout_candidates,
    strong_uptrend,
    near_52w_high
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

st.success(
    "Database Initialized Successfully"
)

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

    st.info(
        "System Ready"
    )

# ==========================
# UNIVERSE LOADER
# ==========================

elif menu == "Universe Loader":

    st.header(
        "📥 NSE Universe Loader"
    )

    st.write(
        "Load NSE stocks into database"
    )

    if st.button(
        "🚀 Load NSE Universe"
    ):

        total = load_nse_universe()

        st.success(
            f"{total} Stocks Loaded"
        )

# ==========================
# MARKET SCANNER
# ==========================

elif menu == "Market Scanner":

    st.header(
        "📡 Market Scanner"
    )

    st.write(
        "Download price data and calculate technical indicators"
    )

    limit = st.slider(
        "Stocks To Scan",
        10,
        500,
        50
    )

    if st.button(
        "🚀 Run Scan"
    ):

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

    st.header(
        "💼 Portfolio"
    )

    st.info(
        "Coming Soon"
    )

# ==========================
# SCREENER
# ==========================

elif menu == "Screener":

    st.header(
        "🔍 Smart Screener"
    )

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
# IPO SCANNER
# ==========================

elif menu == "IPO Scanner":

    st.header(
        "🆕 IPO Discovery"
    )

    st.info(
        "Coming Soon"
    )
