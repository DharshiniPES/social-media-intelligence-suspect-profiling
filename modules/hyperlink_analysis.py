def hyperlink_score(
        links1,
        links2):

    set1 = set(links1)
    set2 = set(links2)

    if len(set1.union(set2)) == 0:
        return 0

    score = (
        len(set1.intersection(set2))
        /
        len(set1.union(set2))
    )

    return round(score, 3)