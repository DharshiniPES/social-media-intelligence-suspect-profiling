class OpenSetRecognizer:

    DEFAULT_THRESHOLD = 0.75

    @staticmethod
    def evaluate(results, threshold=None):

        if threshold is None:
            threshold = OpenSetRecognizer.DEFAULT_THRESHOLD

        if len(results) == 0:

            return {

                "status": "NO_RESULTS",

                "best_match": None

            }

        best = results[0]

        if best["fusion_score"] < threshold:

            return {

                "status": "UNKNOWN",

                "best_match": best,

                "threshold": threshold

            }

        return {

            "status": "MATCH",

            "best_match": best,

            "threshold": threshold

        }