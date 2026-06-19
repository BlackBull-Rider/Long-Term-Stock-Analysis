# core/auto_parameters.py

def generate_parameters(
    years,
    expected_cagr,
    risk="Medium"
):

    result = {}

    # ==========================
    # LOW RISK
    # ==========================

    if risk == "Low":

        result["roe"] = max(
            15,
            expected_cagr
        )

        result["roce"] = max(
            15,
            expected_cagr
        )

        result["debt"] = 0.5

        result["sales_growth"] = 10

        result["profit_growth"] = 10

        result["promoter"] = 50

        result["institutional"] = 10

        result["pe"] = 35

    # ==========================
    # MEDIUM RISK
    # ==========================

    elif risk == "Medium":

        result["roe"] = max(
            18,
            expected_cagr
        )

        result["roce"] = max(
            18,
            expected_cagr
        )

        result["debt"] = 0.75

        result["sales_growth"] = 12

        result["profit_growth"] = 12

        result["promoter"] = 50

        result["institutional"] = 8

        result["pe"] = 50

    # ==========================
    # HIGH RISK
    # ==========================

    elif risk == "High":

        result["roe"] = max(
            20,
            expected_cagr
        )

        result["roce"] = max(
            20,
            expected_cagr
        )

        result["debt"] = 1.0

        result["sales_growth"] = 15

        result["profit_growth"] = 15

        result["promoter"] = 45

        result["institutional"] = 5

        result["pe"] = 80

    # ==========================
    # AGGRESSIVE
    # ==========================

    else:

        result["roe"] = max(
            25,
            expected_cagr
        )

        result["roce"] = max(
            25,
            expected_cagr
        )

        result["debt"] = 2.0

        result["sales_growth"] = 20

        result["profit_growth"] = 20

        result["promoter"] = 40

        result["institutional"] = 0

        result["pe"] = 150

    # ==========================
    # LONG TERM BONUS
    # ==========================

    if years >= 20:

        result["promoter"] += 5

        result["sales_growth"] += 2

        result["profit_growth"] += 2

    if years >= 30:

        result["promoter"] += 5

        result["sales_growth"] += 3

        result["profit_growth"] += 3

    return result
