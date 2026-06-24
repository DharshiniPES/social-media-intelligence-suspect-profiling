def feature_contributions(

    username_score,

    stylometry_score,

    behavior_score,

    temporal_score

):

    contributions = {

        "Username Similarity":
        username_score,

        "Stylometry":
        stylometry_score,

        "Behavior Fingerprint":
        behavior_score,

        "Temporal Pattern":
        temporal_score
    }

    contributions = dict(

        sorted(

            contributions.items(),

            key=lambda x: x[1],

            reverse=True
        )
    )

    return contributions