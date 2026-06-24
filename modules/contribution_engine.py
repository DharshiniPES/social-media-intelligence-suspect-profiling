def get_contribution_data(

    username_score,

    stylometry_score,

    behavior_score,

    temporal_score

):

    return {

        "Username":
        username_score,

        "Stylometry":
        stylometry_score,

        "Behavior":
        behavior_score,

        "Temporal":
        temporal_score
    }