def create_fingerprint(profile):

    post = profile["posts"]

    words = post.split()

    if len(words) > 0:

        avg_word_length = sum(
            len(word)
            for word in words
        ) / len(words)

    else:

        avg_word_length = 0

    post_length = len(post)

    active_hour = profile[
        "active_hours"
    ][0]

    hashtag_count = len(
        profile["hashtags"]
    )

    fingerprint = [

        avg_word_length,

        post_length,

        active_hour,

        hashtag_count

    ]

    return fingerprint


def fingerprint_similarity(

    profile1,
    profile2

):

    fp1 = create_fingerprint(
        profile1
    )

    fp2 = create_fingerprint(
        profile2
    )

    avg1, len1, hour1, hash1 = fp1

    avg2, len2, hour2, hash2 = fp2

    word_sim = 1 - (

        abs(
            avg1 - avg2
        )

        /

        max(
            avg1,
            avg2,
            1
        )

    )

    length_sim = 1 - (

        abs(
            len1 - len2
        )

        /

        max(
            len1,
            len2,
            1
        )

    )

    hour_diff = abs(
        hour1 - hour2
    )

    hour_sim = 1 - (

        min(

            hour_diff,

            24 - hour_diff

        )

        / 12

    )

    hashtag_sim = 1 - (

        abs(
            hash1 - hash2
        )

        /

        max(
            hash1,
            hash2,
            1
        )

    )

    behavior_score = (

        word_sim * 0.25 +

        length_sim * 0.30 +

        hour_sim * 0.25 +

        hashtag_sim * 0.20

    )

    behavior_score = max(
        0,
        min(
            behavior_score,
            1
        )
    )

    return round(
        behavior_score,
        3
    )