from models.origin_region import OriginRegion
from models.order_block import OrderBlock
from assessments.market_configuration import MarketConfiguration

from architecture.selection.candidate_generator import CandidateGenerator
from policies.order_block.base_projection_policy import ProjectionPolicy
from builders.order_block_builder import OrderBlockBuilder
class OrderBlockEngine:

    def __init__(
        self,
        origin_regions: tuple[OriginRegion, ...],
        configuration: MarketConfiguration,
        candidate_generator: CandidateGenerator,
        projection_policy: ProjectionPolicy
    ):

        self.origin_regions = origin_regions
        self.configuration = configuration
        self.candidate_generator = candidate_generator
        self.projection_policy = projection_policy

        self.builder = OrderBlockBuilder()

        self.order_blocks = []

    def build(
        self
    ) -> tuple[OrderBlock, ...]:

        for origin_region in self.origin_regions:

            candidates = self.candidate_generator.generate(
                origin_region,
                self.configuration
            )

            selected = self.projection_policy.select(
                candidates
            )

            order_block = self.builder.build(
                origin_region,
                selected
            )

            self.order_blocks.append(order_block)

        return tuple(self.order_blocks)