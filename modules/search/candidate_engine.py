from typing import List

class CandidateSearchEngine:
    """
    Collects candidate profiles from multiple platforms.
    Every returned profile should already be normalized into
    an EvidenceProfile.
    """

    def __init__(self):
        self.collectors = {}

    def register_collector(self, platform_name, collector):
        """
        Register a platform collector.

        Example:
            engine.register_collector("instagram", InstagramCollector())
        """
        self.collectors[platform_name] = collector

    def search(self, query, platforms=None):
        """
        Search for candidate identities across platforms.

        Parameters
        ----------
        query : str
            Username / email / display name.

        platforms : list
            Platforms to search.
        """

        candidates = []

        if platforms is None:
            platforms = list(self.collectors.keys())

        for platform in platforms:

            if platform not in self.collectors:
                continue

            collector = self.collectors[platform]

            try:

                results = collector.search(query)

                for profile in results:
                    candidates.append(profile)

            except Exception as e:

                print(f"[{platform}] Search failed: {e}")

        return candidates