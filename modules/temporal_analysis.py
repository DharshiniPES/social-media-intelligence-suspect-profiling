def temporal_score(hours1, hours2):

    set1 = set(hours1)
    set2 = set(hours2)

    if len(set1.union(set2)) == 0:
        return 0

    score = (
        len(set1.intersection(set2))
        /
        len(set1.union(set2))
    )

    return round(score, 3)