from abc import ABC, abstractmethod

from models.expansion import Expansion
from assessments.market_configuration import MarketConfiguration
from models.origin_region import OriginRegion


class OriginRegionPolicy(ABC):

    @abstractmethod
    def locate(
        self,
        expansion: Expansion,
        configuration: MarketConfiguration
    ) -> OriginRegion:
        """
        Locate the Origin Region for a confirmed Expansion.

        The returned Origin Region must be:

        - deterministic
        - immutable
        - uniquely associated with the Expansion
          under this policy
        """
        pass