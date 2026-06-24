def risk_level(score):

    if score >= 0.85:

        return "HIGH"

    elif score >= 0.65:

        return "MEDIUM"

    else:

        return "LOW"