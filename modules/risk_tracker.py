def risk_level(score):

    if score >= 0.35:
        return "HIGH"

    elif score >= 0.20:
        return "MEDIUM"

    else:
        return "LOW"