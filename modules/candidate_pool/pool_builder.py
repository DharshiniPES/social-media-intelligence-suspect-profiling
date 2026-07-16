class CandidatePoolBuilder:

    @staticmethod
    def build(live_profiles, repository_profiles):

        pool = []

        pool.extend(live_profiles)

        pool.extend(repository_profiles)

        return pool