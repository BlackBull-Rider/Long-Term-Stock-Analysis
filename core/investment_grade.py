# core/investment_grade.py


def investment_grade(score):

    # ==========================
    # ELITE COMPOUNDER
    # ==========================

    if score >= 95:

        return "STRONG BUY"

    # ==========================
    # HIGH QUALITY
    # ==========================

    elif score >= 80:

        return "BUY"

    # ==========================
    # GOOD BUSINESS
    # ==========================

    elif score >= 65:

        return "ACCUMULATE"

    # ==========================
    # AVERAGE
    # ==========================

    elif score >= 50:

        return "HOLD"

    # ==========================
    # WEAK
    # ==========================

    elif score >= 35:

        return "REDUCE"

    # ==========================
    # POOR
    # ==========================

    else:

        return "AVOID"


def investment_label(score):

    if score >= 95:

        return "🟢 Elite Compounder"

    elif score >= 80:

        return "🟢 High Quality"

    elif score >= 65:

        return "🟡 Growth Candidate"

    elif score >= 50:

        return "🟠 Average"

    elif score >= 35:

        return "🔴 Weak"

    else:

        return "⛔ Avoid"
