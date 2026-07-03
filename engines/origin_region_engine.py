
from policies.origin_region.base_origin_region_policy import (
    OriginRegionPolicy
)

class OriginRegionEngine:

    def __init__(

        self,

        expansions,

        configuration,

        policy: OriginRegionPolicy

    ):

        self.expansions = expansions
        self.configuration = configuration
        self.policy = policy

        self.origin_regions = []

    def build(self):

        for expansion in self.expansions:

            region = self.policy.locate(
                expansion,
                self.configuration
            )

            if region is not None:
                self.origin_regions.append(region)

        return tuple(self.origin_regions)