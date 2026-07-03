from abc import ABC, abstractmethod


class FairValueGapPolicy(ABC):

    @abstractmethod
    def detect(
        self,
        configuration
    ):
        """
        Detect Fair Value Gaps.

        Returns
        -------
        tuple[FairValueGap, ...]
        """
        pass