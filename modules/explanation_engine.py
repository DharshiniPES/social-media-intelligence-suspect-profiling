def generate_explanation(

    username_score,

    stylometry_score,

    behavior_score,

    temporal_score

):

    reasons = []

    if username_score >= 0.5:

        reasons.append(
            "High username similarity"
        )

    if stylometry_score >= 0.7:

        reasons.append(
            "Similar writing style"
        )

    if behavior_score >= 0.8:

        reasons.append(
            "Matching behavioral fingerprint"
        )

    if temporal_score >= 0.8:

        reasons.append(
            "Similar activity pattern"
        )

    if len(reasons) == 0:

        reasons.append(
            "Weak evidence"
        )

    return reasons
