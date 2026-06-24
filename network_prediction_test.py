import json

from modules.username_similarity import username_score
from modules.bio_similarity import bio_score
from modules.stylometry import stylometry_score
from modules.emoji_analysis import emoji_score
from modules.temporal_analysis import temporal_score
from modules.hyperlink_analysis import hyperlink_score
from modules.hashtag_analysis import hashtag_score

from fusion.fusion_engine import fusion_score

from modules.network_analysis import (
    build_graph,
    add_link,
    draw_graph
)


with open(
    "data/profiles.json",
    "r",
    encoding="utf-8"
) as file:

    profiles = json.load(file)


G = build_graph(
    profiles
)


for i in range(len(profiles)):

    for j in range(i + 1, len(profiles)):

        profile1 = profiles[i]
        profile2 = profiles[j]

        user_score = username_score(
            profile1["username"],
            profile2["username"]
        )

        bio_similarity = bio_score(
            profile1["bio"],
            profile2["bio"]
        )

        style_score = stylometry_score(
            profile1["posts"],
            profile2["posts"]
        )

        emoji_similarity = emoji_score(
            profile1["posts"],
            profile2["posts"]
        )

        temporal_similarity = temporal_score(
            profile1["active_hours"],
            profile2["active_hours"]
        )

        link_similarity = hyperlink_score(
            profile1["links"],
            profile2["links"]
        )

        hashtag_similarity = hashtag_score(
            profile1["hashtags"],
            profile2["hashtags"]
        )

        final_score = fusion_score(

            user_score,

            bio_similarity,

            style_score,

            emoji_similarity,

            temporal_similarity,

            link_similarity,

            hashtag_similarity
        )

        if final_score >= 0.65:

            add_link(

                G,

                profile1["id"],
                profile2["id"],

                final_score
            )


draw_graph(G)