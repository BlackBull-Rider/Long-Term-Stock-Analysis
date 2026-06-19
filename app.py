# app.py

import streamlit as st

from database.schema import create_tables

from core.screener import (
    long_term_screener,
    swing_screener,
    top_compounders,
    top_breakouts,
    institutional_picks
)

from core.ipo_engine import (
    get_top_ipos
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

from core.recommendation_data import (
    load_recommendation_data
)

from core.recommendation_engine import (
    generate_recommendations
)

from core.stock_analysis_engine import (
    analyze_stock
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

st.title(
    "🦅 Green Bull Rider V6"
)


# ==========================
# MENU
# ==========================

menu = st.sidebar.selectbox(

    "Navigation",

    [

        "Dashboard",

        "Long Term Screener",

        "Swing Screener",

        "IPO Hunter",

        "Portfolio",

        "Portfolio Analysis",

        "AI Recommendation",

        "Stock Analysis"

    ]

)


# ==========================
# DASHBOARD
# ==========================

if menu == "Dashboard":

    st.header(
        "📊 Dashboard"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Top Compounders",
            len(
                top_compounders()
            )
        )

    with col2:

        st.metric(
            "Top Breakouts",
            len(
                top_breakouts()
            )
        )

    with col3:

        st.metric(
            "Institutional Picks",
            len(
                institutional_picks()
            )
        )

    st.divider()

    st.subheader(
        "🏆 Top Compounders"
    )

    st.dataframe(
        top_compounders().head(20),
        use_container_width=True
    )

    st.subheader(
        "🚀 Top Breakouts"
    )

    st.dataframe(
        top_breakouts().head(20),
        use_container_width=True
    )


# ==========================
# LONG TERM
# ==========================

elif menu == "Long Term Screener":

    st.header(
        "🏆 Long Term Screener"
    )

    df = long_term_screener()

    st.write(
        f"Found {len(df)} Stocks"
    )

    st.dataframe(
        df,
        use_container_width=True
    )


# ==========================
# SWING
# ==========================

elif menu == "Swing Screener":

    st.header(
        "⚡ Swing Screener"
    )

    df = swing_screener()

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

elif menu == "IPO Hunter":

    st.header(
        "🚀 IPO Hunter"
    )

    df = get_top_ipos()

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning(
            "No IPO Data Available"
        )


# ==========================
# PORTFOLIO
# ==========================

elif menu == "Portfolio":

    st.header(
        "💼 Portfolio"
    )

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

    with tab1:

        selected_stock = st.selectbox(
            "Search Stock",
            stock_options,
            index=None
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

        if st.button(
            "Buy Stock"
        ):

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

        if st.button(
            "Sell Stock"
        ):

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

    with tab3:

        st.dataframe(
            holdings,
            use_container_width=True
        )

        st.dataframe(
            get_transactions(),
            use_container_width=True
        )


# ==========================
# PORTFOLIO ANALYSIS
# ==========================

elif menu == "Portfolio Analysis":

    st.header(
        "📈 Portfolio Analysis"
    )

    st.info(
        "Institutional Portfolio Analytics Coming Soon"
    )


# ==========================
# AI RECOMMENDATION
# ==========================

elif menu == "AI Recommendation":

    st.header(
        "🤖 AI Recommendation"
    )

    years = st.slider(
        "Investment Horizon",
        1,
        30,
        10
    )

    expected_return = st.slider(
        "Expected CAGR (%)",
        10,
        100,
        20
    )

    if st.button(
        "Generate Recommendations"
    ):

        df = load_recommendation_data()

        result = generate_recommendations(
            df,
            years,
            expected_return
        )

        st.dataframe(
            result,
            use_container_width=True
        )


# ==========================
# STOCK ANALYSIS
# ==========================

elif menu == "Stock Analysis":

    st.header(
        "📈 Stock Analysis"
    )

    stock_options = get_stock_options()

    selected = st.selectbox(
        "Select Stock",
        stock_options,
        index=None
    )

    if selected:

        symbol = (
            selected
            .split(" - ")[0]
        )

        result = analyze_stock(
            symbol
        )

        if result:

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "CMP",
                result["cmp"]
            )

            c2.metric(
                "Target",
                result["target"]
            )

            c3.metric(
                "Stoploss",
                result["stoploss"]
            )

            st.success(
                f"Action : {result['action']}"
            )

            st.write(
                f"Overall Score : {result['overall']}"
            )

            st.write(
                f"Grade : {result['grade']}"
            )

            st.dataframe(
                [result],
                use_container_width=True
            )
