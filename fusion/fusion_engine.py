def fusion_score(

    username_score,

    bio_score,

    stylometry_score,

    behavior_score,

    emoji_score,

    temporal_score,

    hyperlink_score,

    hashtag_score

):

    score = (

        0.15 * username_score +

        0.10 * bio_score +

        0.20 * stylometry_score +

        0.10 * behavior_score +

        0.10 * emoji_score +

        0.10 * temporal_score +

        0.10 * hyperlink_score +

        0.15 * hashtag_score

    )

    return round(
        score,
        3
    )