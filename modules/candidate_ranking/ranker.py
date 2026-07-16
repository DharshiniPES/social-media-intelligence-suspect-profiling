class CandidateRanker:

    @staticmethod
    def rank(results):

        ranked = []

        for i, result in enumerate(results, start=1):

            candidate = result["candidate"]

            ranked.append({

                "rank": i,

                "username": candidate.username,

                "platform": candidate.platform,

                "fusion_score": result["fusion_score"],

                "result": result

            })

        return ranked