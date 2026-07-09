def fusion_score(scores, reliability):
    """
    Adaptive fusion using evidence reliability.

    scores:
        Dictionary of similarity scores.

    reliability:
        Dictionary of evidence reliability scores.
    """

    weighted_sum = 0.0
    total_weight = 0.0

    for feature in scores:

        score = scores.get(feature, 0.0)

        weight = reliability.get(feature, 0.0)

        # Ignore modules that have no usable evidence
        if weight <= 0:
            continue

        weighted_sum += score * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(weighted_sum / total_weight, 3)