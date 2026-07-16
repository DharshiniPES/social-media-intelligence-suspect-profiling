from pipeline.comparison_engine import ComparisonEngine


class RankingPipeline:

    @staticmethod
    def rank(target_profile, candidates):

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