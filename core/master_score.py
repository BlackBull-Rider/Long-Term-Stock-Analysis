# core/master_score.py

def master_score(row):

    compounder = row.get(
        "Compounder Score",
        0
    )

    breakout = row.get(
        "Breakout Score",
        0
    )

    institutional = row.get(
        "Institutional Score",
        0
    )

    ipo = row.get(
        "IPO Score",
        0
    )

    score = (

        compounder * 0.40

        +

        breakout * 0.25

        +

        institutional * 0.20

        +

        ipo * 0.15

    )

    return round(
        score,
        2
    )


def master_grade(score):

    if score >= 85:
        return "🏆 Elite"

    if score >= 70:
        return "🥇 Strong Buy"

    if score >= 55:
        return "🥈 Buy"

    if score >= 40:
        return "🥉 Watchlist"

    return "⚪ Ignore"
