import jellyfish

def username_score(user1, user2):

    score = jellyfish.jaro_winkler_similarity(
        user1.lower(),
        user2.lower()
    )

    return score