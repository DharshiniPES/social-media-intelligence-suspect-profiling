class CandidateDeduplicator:

    @staticmethod
    def deduplicate(candidates):

        unique = {}

        for candidate in candidates:

            key = (

                candidate.platform.lower(),

                candidate.username.lower()

            )

            if key not in unique:

                unique[key] = candidate

        return list(unique.values())