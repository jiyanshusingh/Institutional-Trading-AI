from abc import ABC, abstractmethod

from models.expansion import Expansion
from models.origin_region import OriginRegion


class OriginRegionPolicy(ABC):

    @abstractmethod
    def identify(
        self,
        expansion: Expansion,
        df
    ) -> OriginRegion | None:
        """
        Identify the Origin Region for the given Expansion.

        Returns:
            OriginRegion if found.
            None otherwise.
        """
        pass