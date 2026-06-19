# core/smart_screener.py

import pandas as pd

from core.auto_parameters import (
    generate_parameters
)

from core.compounder_engine import (
    calculate_compounder_score
)


def run_screener(
    df,
    years,
    expected_cagr,
    risk="Medium"
):

    if df.empty:
        return df

    params = generate_parameters(
        years,
        expected_cagr,
        risk
    )

    df = df.copy()

    numeric_cols = [

        "roe",
        "roce",

        "debt_equity",

        "sales_growth",
        "profit_growth",

        "pe",
        "pb",

        "institutional_holding"

    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    df = df.fillna(0)

    # ==========================
    # FUNDAMENTAL FILTER
    # ==========================

    filtered = df[

        (df["roe"] >= params["roe"])

        &

        (df["roce"] >= params["roce"])

        &

        (
            df["debt_equity"]
            <=
            params["debt"]
        )

        &

        (
            df["sales_growth"]
            >=
            params["sales_growth"]
        )

        &

        (
            df["profit_growth"]
            >=
            params["profit_growth"]
        )

    ]

    if filtered.empty:

        return filtered

    # ==========================
    # COMPOUNDER SCORE
    # ==========================

    filtered[
        "Compounder Score"
    ] = filtered.apply(
        calculate_compounder_score,
        axis=1
    )

    # ==========================
    # QUALITY SCORE
    # ==========================

    filtered[
        "Quality Score"
    ] = (

        filtered["roe"] * 0.25

        +

        filtered["roce"] * 0.25

        +

        filtered["sales_growth"] * 0.20

        +

        filtered["profit_growth"] * 0.20

        +

        filtered.get(
            "institutional_holding",
            0
        ) * 0.10

    )

    # ==========================
    # EXPECTED CAGR
    # ==========================

    filtered[
        "Expected CAGR"
    ] = (

        filtered["roe"] * 0.35

        +

        filtered["roce"] * 0.25

        +

        filtered["sales_growth"] * 0.20

        +

        filtered["profit_growth"] * 0.20

    )

    # ==========================
    # FINAL SCORE
    # ==========================

    filtered[
        "Final Score"
    ] = (

        filtered["Compounder Score"]

        +

        filtered["Quality Score"]

    ) / 2

    filtered = filtered.sort_values(

        by="Final Score",

        ascending=False

    )

    return filtered.head(100)
