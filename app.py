import streamlit as st

from database.schema import create_tables
from data.load_universe import load_nse_universe

# =========================
# DATABASE INIT
# =========================

create_tables()

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Green Bull Rider V6",
    page_icon="🦅",
    layout="wide"
)

# =========================
# HEADER
# =========================

st.title("🦅 Green Bull Rider V6")

st.success(
    "Database Initialized Successfully"
)

# =========================
# SIDEBAR
# =========================

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Universe Loader",
        "Portfolio",
        "Screener",
        "IPO Scanner"
    ]
)

# =========================
# DASHBOARD
# =========================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    st.info(
        "System Ready"
    )

# =========================
# UNIVERSE LOADER
# =========================

elif menu == "Universe Loader":

    st.header(
        "📥 NSE Universe Loader"
    )

    st.write(
        "Load all NSE stocks into database"
    )

    if st.button(
        "🚀 Load NSE Universe"
    ):

        with st.spinner(
            "Loading NSE Universe..."
        ):

            total = load_nse_universe()

        st.success(
            f"{total} Stocks Loaded Successfully"
        )

# =========================
# PORTFOLIO
# =========================

elif menu == "Portfolio":

    st.header(
        "💼 Portfolio"
    )

    st.info(
        "Coming Soon"
    )

# =========================
# SCREENER
# =========================

elif menu == "Screener":

    st.header(
        "🔍 Smart Screener"
    )

    st.info(
        "Coming Soon"
    )

# =========================
# IPO SCANNER
# =========================

elif menu == "IPO Scanner":

    st.header(
        "🆕 IPO Discovery"
    )

    st.info(
        "Coming Soon"
    )
