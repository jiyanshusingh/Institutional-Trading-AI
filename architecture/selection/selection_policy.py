from abc import ABC, abstractmethod


class SelectionPolicy(ABC):

    @abstractmethod
    def select(
        self,
        candidates
    ):
        """
        Select one candidate from the candidate set.
        """
        pass