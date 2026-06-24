def bot_risk_score(followers, retweets, verified):
    score = 0

    if followers < 50:
        score += 0.4

    if retweets > 500:
        score += 0.3

    if not verified:
        score += 0.3

    return min(score, 1.0)