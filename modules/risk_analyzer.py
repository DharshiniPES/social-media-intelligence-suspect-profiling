def website_risk(profile):

    score = 0

    security = profile.get("security", {})

    if not security.get("HTTPS", False):

        score += 25

    if not security.get("CSP", False):

        score += 15

    if not security.get("HSTS", False):

        score += 15

    if len(profile.get("emails", [])):

        score += 10

    if len(profile.get("phones", [])):

        score += 10

    return min(score,100)