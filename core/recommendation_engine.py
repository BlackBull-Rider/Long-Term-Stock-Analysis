# core/recommendation_engine.py

import pandas as pd

from core.auto_parameters import (
    generate_parameters
)

from core.compounder_engine import (
    calculate_compounder_score
)

from core.master_score import (
    master_score,
    master_grade
)


def generate_recommendations(
    df,
    years,
    expected_return
):

    if df.empty:
        return df

    params = generate_parameters(
        years,
        expected_return
    )

    df = df.copy()

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
    # DEFAULT SCORES
    # ==========================

    if (
        "Breakout Score"
        not in filtered.columns
    ):
        filtered[
            "Breakout Score"
        ] = 0

    if (
        "Institutional Score"
        not in filtered.columns
    ):
        filtered[
            "Institutional Score"
        ] = 0

    if (
        "IPO Score"
        not in filtered.columns
    ):
        filtered[
            "IPO Score"
        ] = 0

    # ==========================
    # MASTER SCORE
    # ==========================

    filtered[
        "Master Score"
    ] = filtered.apply(
        master_score,
        axis=1
    )

    filtered[
        "Recommendation"
    ] = filtered[
        "Master Score"
    ].apply(
        master_grade
    )

    filtered = filtered.sort_values(

        by="Master Score",

        ascending=False

    )

    return filtered.head(20)
