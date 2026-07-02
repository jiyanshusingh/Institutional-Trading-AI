from abc import ABC, abstractmethod

from models.origin_region import OriginRegion
from models.order_block import OrderBlock


class OrderBlockPolicy(ABC):

    @abstractmethod
    def create(
        self,
        origin_region: OriginRegion,
        df
    ) -> OrderBlock:
        pass