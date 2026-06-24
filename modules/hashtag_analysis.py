def hashtag_score(
        hashtags1,
        hashtags2):

    set1 = set(hashtags1)
    set2 = set(hashtags2)

    if len(set1.union(set2)) == 0:
        return 0

    score = (
        len(set1.intersection(set2))
        /
        len(set1.union(set2))
    )

    return round(score, 3)