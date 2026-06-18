def investment_grade(score):

    if score >= 85:
        return "A+ Compounder"

    if score >= 70:
        return "A Grade"

    if score >= 55:
        return "B Grade"

    if score >= 40:
        return "C Grade"

    return "Avoid"
