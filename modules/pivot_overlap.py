def calculate_pivot_boost(profile1, profile2):
    """
    Returns a float (0.0 to 0.5) to boost fusion score 
    if hard identifiers match.
    """
    boost = 0.0
    # Match Emails
    if set(profile1.emails) & set(profile2.emails):
        boost += 0.30
    # Match Domains
    if set(profile1.hyperlinks) & set(profile2.hyperlinks):
        boost += 0.20
    return min(0.5, boost)