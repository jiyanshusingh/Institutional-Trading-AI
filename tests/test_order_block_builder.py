from engines.data_engine import DataEngine
from services.market_analysis_engine import MarketAnalysisEngine

from policies.order_block.ict.ict_order_block_candidate_generator import (
    ICTOrderBlockCandidateGenerator
)

from policies.order_block.ict.ict_projection_policy import (
    ICTProjectionPolicy
)

from builders.order_block_builder import (
    OrderBlockBuilder
)


def main():

    # Build Market Configuration
    data = DataEngine()

    df = data.get_data(
        "RELIANCE.NS",
        period="1y",
        interval="1d"
    )

    engine = MarketAnalysisEngine()

    configuration = engine.analyze(df)

    # Origin Region
    origin_region = configuration.origin_regions[0]

    # Candidate Generation
    generator = ICTOrderBlockCandidateGenerator()

    candidates = generator.generate(
        origin_region,
        configuration
    )

    # Candidate Selection
    policy = ICTProjectionPolicy()

    selected_candidate = policy.select(
        candidates
    )

    # Build Order Block
    builder = OrderBlockBuilder()

    order_block = builder.build(
        origin_region,
        selected_candidate
    )

    print()

    print("=========================")
    print("ORDER BLOCK BUILDER")
    print("=========================")
    print()

    print("Origin Region")
    print("-------------")
    print(origin_region)

    print()

    print("Selected Candidate")
    print("------------------")
    print(selected_candidate)

    print()

    print("Order Block")
    print("-----------")
    print(order_block)


if __name__ == "__main__":
    main()