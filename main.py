import json
from modules.feature_contribution import (
    feature_contributions
)
from modules.behavioral_fingerprint import (
    fingerprint_similarity
)
from modules.explanation_engine import (
    generate_explanation
)
from database.db_manager import DatabaseManager
from evaluation import *
from modules.hashtag_analysis import hashtag_score
from modules.hyperlink_analysis import hyperlink_score
from modules.username_similarity import username_score
from modules.bio_similarity import bio_score
from modules.stylometry import stylometry_score
from modules.emoji_analysis import emoji_score
from modules.temporal_analysis import temporal_score
from modules.bot_risk_analysis import bot_risk_score
from modules.network_analysis import (
    build_graph,
    add_link,
    draw_graph,
    detect_communities
)

from fusion.fusion_engine import fusion_score

tp = 0
fp = 0
fn = 0
tn = 0
with open(
    "data/profiles.json",
    "r",
    encoding="utf-8"
) as file:

    from modules.real_dataset_loader import RealDatasetLoader

    loader = RealDatasetLoader(
        "datasets/real/bot_detection_data.csv"
    )

    profiles = loader.load_profiles()

db = DatabaseManager()

db.create_tables()
G = build_graph(profiles)

for i in range(len(profiles)):

    for j in range(i + 1, len(profiles)):

        profile1 = profiles[i]
        profile2 = profiles[j]

        user_score = username_score(
            profile1["username"],
            profile2["username"]
        )

        bio_similarity = 0

        style_score = stylometry_score(
            profile1["posts"],
            profile2["posts"]
        )
        behavior_score = fingerprint_similarity(
            profile1,
            profile2
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
            behavior_score,
            emoji_similarity,
            temporal_similarity,
            link_similarity,
            hashtag_similarity
        )
        explanations = generate_explanation(

            user_score,

            style_score,

            behavior_score,

            temporal_similarity

        )
        contributions = feature_contributions(

            user_score,

            style_score,

            behavior_score,

            temporal_similarity
        )
        explanation_text = ", ".join(
            explanations
        )
        risk_score = bot_risk_score(
            profile1["followers"],
            profile1["retweets"],
            profile1["verified"]
        )
        print("Bot Risk Score:", round(risk_score, 3))
        print("\n========================================")
        print(
            f"{profile1['id']} vs {profile2['id']}"
        )
        print("========================================")

        print(
            "Username Score:",
            round(user_score, 3)
        )

        print(
            "Bio Score:",
            round(bio_similarity, 3)
        )

        print(
            "Stylometry Score:",
            round(style_score, 3)
        )
        print(
            "Behavior Score:",
            round(behavior_score, 3)
        )

        print(
            "Emoji Score:",
            round(emoji_similarity, 3)
        )

        print(
            "Temporal Score:",
            round(temporal_similarity, 3)
        )
        print(
            "Hyperlink Score:",
            round(link_similarity, 3)
        )
        print(
            "Hashtag Score:",
            round(hashtag_similarity, 3)
        )
        print(
            "Fusion Score:",
            round(final_score, 3)
        )
        print(
            "Explanation:"
        )
        for reason in explanations:

            print(
                "-",
                reason
            )
        print(
            "\nFeature Contributions:"
        )

        for feature, score in contributions.items():

            print(
                f"{feature}: {round(score,3)}"
            )

        print(
            "Confidence:",
            round(final_score * 100, 2),
            "%"
        )
        print("\n===================")
        print("FINAL EVALUATION")
        print("===================")

        p = precision(tp, fp)
        r = recall(tp, fn)
        f1 = f1_score(p, r)

        print("True Positives :", tp)
        print("False Positives:", fp)
        print("False Negatives:", fn)
        print("True Negatives :", tn)

        print("Precision:", round(p, 3))
        print("Recall:", round(r, 3))
        print("F1 Score:", round(f1, 3))

        predicted =(
            final_score >= 0.45
        )

        db.insert_comparison(

             
            profile1["id"],
            profile2["id"],

            user_score,
            bio_similarity,
            style_score,
            emoji_similarity,
            temporal_similarity,
            link_similarity,
            hashtag_similarity,
            behavior_score,
            final_score,
            explanation_text,
            int(predicted)
        )
        actual = False
        #if predicted and actual:

        #    tp += 1

        #elif predicted and not actual:

        #    fp += 1

        #elif not predicted and actual:

        #   fn += 1

        #else:

        #   tn += 1
        print("FINAL SCORE =", final_score)
        print("PREDICTED =", predicted)
        if predicted:

            add_link(
                G,
                profile1["id"],
                profile2["id"],
                final_score
            )

            print("LINKED")

        else:

            print("NOT LINKED")
draw_graph(G)

communities = detect_communities(G)

print("\n=== COMMUNITIES ===")

for i, community in enumerate(
    communities,
    start=1
):

    print(
        f"Community {i}:",
        list(community)
    )

print(
    "\nNetwork graph generated."
)