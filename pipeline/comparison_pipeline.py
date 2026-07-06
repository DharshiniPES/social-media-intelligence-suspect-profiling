from modules.stylometry import stylometry_score
from modules.pivot_analyzer import calculate_pivot_similarity
from modules.username_similarity import username_score
from modules.bio_similarity import bio_score
from pipeline.adapters import github_to_profile
from modules.behavioral_fingerprint import fingerprint_similarity
class ComparisonPipeline:

    def compare(self, evidence1, evidence2):

        results = {}

        # Stylometry
        results["stylometry"] = stylometry_score(
            evidence1["content"],
            evidence2["content"]
        )
        # Username Similarity

        results["username_similarity"] = username_score(
            evidence1["identity"]["username"],
            evidence2["identity"]["username"]
        )
        # Bio Similarity

        results["bio_similarity"] = bio_score(

            evidence1["identity"]["bio"],

            evidence2["identity"]["bio"]

        )
        # Behavioral Fingerprint

        profile1 = github_to_profile(

            evidence1["metadata"]

        )

        profile2 = github_to_profile(

            evidence2["metadata"]

        )

        results["behavior"] = fingerprint_similarity(

            profile1,

            profile2

        )
        # Pivot Analysis
        results["pivot_similarity"] = calculate_pivot_similarity(
            evidence1["analysis"]["pivots"],
            evidence2["analysis"]["pivots"]
        )

        return results