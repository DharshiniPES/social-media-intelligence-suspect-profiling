from modules.search.candidate_engine import CandidateSearchEngine

class SearchManager:

    def __init__(self):

        self.engine = CandidateSearchEngine()

    def register_platform(self, name, collector):

        self.engine.register_collector(name, collector)

    def search(self, query, platforms):

        return self.engine.search(query, platforms)