# core/auto_parameters.py

def generate_parameters(
    years,
    expected_return
):

    result = {}

    # ==========================
    # ULTRA CONSERVATIVE
    # ==========================

    if years >= 20 and expected_return <= 15:

        result["roe"] = 15
        result["roce"] = 15
        result["debt"] = 1.0
        result["sales_growth"] = 8
        result["profit_growth"] = 8
        result["promoter"] = 40
        result["institutional"] = False
        result["margin_safety"] = 10

    # ==========================
    # COMPOUNDER
    # ==========================

    elif years >= 10 and expected_return <= 25:

        result["roe"] = 18
        result["roce"] = 18
        result["debt"] = 0.5
        result["sales_growth"] = 12
        result["profit_growth"] = 12
        result["promoter"] = 50
        result["institutional"] = True
        result["margin_safety"] = 15

    # ==========================
    # HIGH GROWTH
    # ==========================

    elif years >= 10 and expected_return <= 40:

        result["roe"] = 22
        result["roce"] = 20
        result["debt"] = 0.3
        result["sales_growth"] = 18
        result["profit_growth"] = 18
        result["promoter"] = 55
        result["institutional"] = True
        result["margin_safety"] = 20

    # ==========================
    # MULTIBAGGER
    # ==========================

    elif expected_return <= 75:

        result["roe"] = 25
        result["roce"] = 25
        result["debt"] = 0.2
        result["sales_growth"] = 25
        result["profit_growth"] = 25
        result["promoter"] = 60
        result["institutional"] = True
        result["margin_safety"] = 25

    # ==========================
    # SUPER COMPOUNDER
    # ==========================

    else:

        result["roe"] = 30
        result["roce"] = 30
        result["debt"] = 0.0
        result["sales_growth"] = 35
        result["profit_growth"] = 35
        result["promoter"] = 65
        result["institutional"] = True
        result["margin_safety"] = 30

    return result
