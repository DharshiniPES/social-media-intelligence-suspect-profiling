from datetime import datetime

from modules.username_similarity import username_score
from modules.bio_similarity import bio_score
from modules.stylometry import stylometry_score
from modules.emoji_analysis import emoji_score
from modules.behavioral_fingerprint import fingerprint_similarity
from modules.temporal_analysis import temporal_score
from modules.hyperlink_analysis import hyperlink_score
from modules.hashtag_analysis import hashtag_score
from reliability.reliability_engine import ReliabilityEngine
from fusion.fusion_engine import fusion_score
from modules.explanation_engine import generate_explanation

from pipeline.adapters import evidence_to_behavior_profile


class ComparisonEngine:
    """
    Runs all forensic modules on two EvidenceProfile objects.
    Returns module scores, fusion score and explainability.
    """

    @staticmethod
    def _extract_hours(timestamps):
        hours = []

        for ts in timestamps:
            try:
                hours.append(
                    datetime.fromisoformat(ts).hour
                )
            except Exception:
                continue

        return hours

    @staticmethod
    def compare(profile1, profile2):

        # -----------------------------------
        # Username
        # -----------------------------------
        username = username_score(
            profile1.username,
            profile2.username
        )

        # -----------------------------------
        # Bio
        # -----------------------------------
        bio = bio_score(
            profile1.bio,
            profile2.bio
        )

        # -----------------------------------
        # Stylometry
        # -----------------------------------
        text1 = profile1.bio + "\n" + "\n".join(profile1.captions)
        text2 = profile2.bio + "\n" + "\n".join(profile2.captions)

        stylometry = stylometry_score(
            text1,
            text2
        )

        # -----------------------------------
        # Emoji
        # -----------------------------------
        emoji = emoji_score(
            text1,
            text2
        )

        # -----------------------------------
        # Behaviour
        # -----------------------------------
        behaviour = fingerprint_similarity(
            evidence_to_behavior_profile(profile1),
            evidence_to_behavior_profile(profile2)
        )

        # -----------------------------------
        # Temporal
        # -----------------------------------
        temporal = temporal_score(
            ComparisonEngine._extract_hours(profile1.timestamps),
            ComparisonEngine._extract_hours(profile2.timestamps)
        )

        # -----------------------------------
        # Hyperlinks
        # -----------------------------------
        hyperlink = hyperlink_score(
            profile1.hyperlinks,
            profile2.hyperlinks
        )

        # -----------------------------------
        # Hashtags
        # -----------------------------------
        hashtag = hashtag_score(
            profile1.hashtags,
            profile2.hashtags
        )

        # -----------------------------------
        # Fusion
        # -----------------------------------
        # -----------------------------------
        # Build score dictionary
        # -----------------------------------

        scores = {
            "username": username,
            "bio": bio,
            "stylometry": stylometry,
            "behaviour": behaviour,
            "emoji": emoji,
            "temporal": temporal,
            "hyperlink": hyperlink,
            "hashtag": hashtag
        }

        # -----------------------------------
        # Compute evidence reliability
        # -----------------------------------

        reliability1 = ReliabilityEngine.compute(profile1)
        reliability2 = ReliabilityEngine.compute(profile2)

        # -----------------------------------
        # Merge reliability
        # -----------------------------------

        reliability = {}

        for feature in scores:

            reliability[feature] = min(
                reliability1.get(feature, 0),
                reliability2.get(feature, 0)
            )

        # -----------------------------------
        # Adaptive Fusion
        # -----------------------------------

        fusion = fusion_score(
            scores,
            reliability
        )

        # -----------------------------------
        # Explainability
        # -----------------------------------
        explanation = generate_explanation(
            username,
            stylometry,
            behaviour,
            temporal
        )

        return {

            "username_score": round(username, 3),

            "bio_score": round(bio, 3),

            "stylometry_score": round(stylometry, 3),

            "emoji_score": round(emoji, 3),

            "behaviour_score": round(behaviour, 3),

            "temporal_score": round(temporal, 3),

            "hyperlink_score": round(hyperlink, 3),

            "hashtag_score": round(hashtag, 3),

            "fusion_score": round(fusion, 3),

            "explanation": explanation

        }