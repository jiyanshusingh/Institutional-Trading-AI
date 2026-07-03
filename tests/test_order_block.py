from engines.data_engine import DataEngine
from services.market_analysis_engine import MarketAnalysisEngine

from engines.order_block_engine import OrderBlockEngine

from policies.order_block.ict.ict_order_block_candidate_generator import (
    ICTOrderBlockCandidateGenerator
)

from policies.order_block.ict.ict_projection_policy import (
    ICTProjectionPolicy
)


def main():

    data = DataEngine()

    df = data.get_data(
        "RELIANCE.NS",
        period="1y",
        interval="1d"
    )

    engine = MarketAnalysisEngine()

    configuration = engine.analyze(df)

    order_block_engine = OrderBlockEngine(

        origin_regions=configuration.origin_regions,

        configuration=configuration,

        candidate_generator=ICTOrderBlockCandidateGenerator(),

        projection_policy=ICTProjectionPolicy()

    )

    order_blocks = order_block_engine.build()

    print()

    print("===================")
    print("ORDER BLOCK ENGINE")
    print("===================")

    print()

    print("Origin Regions")
    print("--------------")

    for region in configuration.origin_regions:
        print(region)

    print()

    print("Order Blocks")
    print("------------")

    for block in order_blocks:
        print(block)


if __name__ == "__main__":
    main()