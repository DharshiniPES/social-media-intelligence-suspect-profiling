from abc import ABC, abstractmethod

class BaseCollector(ABC):

    @abstractmethod
    def search(self, query):
        """
        Return a list of EvidenceProfiles.
        """
        pass