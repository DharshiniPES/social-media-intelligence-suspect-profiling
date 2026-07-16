from pipeline.search_pipeline import SearchPipeline
from pipeline.comparison_engine import ComparisonEngine


class InvestigatorPipeline:
    """
    Main investigator workflow.

    Search

        ↓

    Normalize

        ↓

    Compare

        ↓

    Rank

        ↓

    Return
    """

    @staticmethod
    def investigate(target_profile, query):

        candidates = SearchPipeline.search(query)

        results = []

        for candidate in candidates:

            comparison = ComparisonEngine.compare(
                target_profile,
                candidate
            )

            comparison["candidate"] = candidate

            results.append(comparison)

        results.sort(
            key=lambda x: x["fusion_score"],
            reverse=True
        )

        return results