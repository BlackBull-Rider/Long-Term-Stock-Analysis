# core/master_score.py


def master_score(row):

    compounder = float(

        row.get(
            "Compounder Score",
            0
        )

    )

    breakout = float(

        row.get(
            "Breakout Score",
            0
        )

    )

    institutional = float(

        row.get(
            "Institutional Score",
            0
        )

    )

    ipo = float(

        row.get(
            "IPO Score",
            0
        )

    )

    score = (

        compounder * 0.45

        +

        breakout * 0.20

        +

        institutional * 0.25

        +

        ipo * 0.10

    )

    return round(
        score,
        2
    )


def master_grade(score):

    if score >= 90:

        return "🟢 STRONG BUY"

    elif score >= 75:

        return "🟢 BUY"

    elif score >= 60:

        return "🟡 ACCUMULATE"

    elif score >= 45:

        return "🟠 HOLD"

    elif score >= 30:

        return "🔴 REDUCE"

    else:

        return "⛔ AVOID"


def recommendation_color(score):

    if score >= 90:

        return "green"

    elif score >= 75:

        return "lightgreen"

    elif score >= 60:

        return "yellow"

    elif score >= 45:

        return "orange"

    else:

        return "red"
