# core/patterns.py

def resistance_breakout(cmp, high52):

    if cmp >= high52:
        return "🚀 52W Breakout"

    if cmp >= high52 * 0.98:
        return "⚡ Near Breakout"

    return "⏸ Normal"


def trend_status(
    cmp,
    ema20,
    ema50,
    ema200
):

    if (
        cmp > ema20
        and
        ema20 > ema50
        and
        ema50 > ema200
    ):
        return "📈 Strong Uptrend"

    if (
        cmp > ema50
        and
        ema50 > ema200
    ):
        return "🟢 Uptrend"

    if cmp > ema200:
        return "🟡 Recovery"

    return "🔴 Weak"


def valuation_tag(
    cmp,
    high52,
    low52
):

    midpoint = (
        high52 + low52
    ) / 2

    if cmp < midpoint * 0.8:
        return "🟢 Discount"

    if cmp > midpoint * 1.2:
        return "🟠 Premium"

    return "⚪ Fair"
