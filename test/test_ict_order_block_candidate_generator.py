from engines.data_engine import DataEngine
from services.market_analysis_engine import MarketAnalysisEngine

from policies.order_block.ict.ict_order_block_candidate_generator import (
    ICTOrderBlockCandidateGenerator
)


def main():

    # Get market configuration
    data = DataEngine()

    df = data.get_data(
        "RELIANCE.NS",
        period="1y",
        interval="1d"
    )

    engine = MarketAnalysisEngine()

    configuration = engine.analyze(df)

    # Get first Origin Region
    origin_region = configuration.origin_regions[0]

    # Candidate Generator
    generator = ICTOrderBlockCandidateGenerator()

    candidates = generator.generate(
        origin_region,
        configuration
    )

    print()
    print("==============================")
    print("ORDER BLOCK CANDIDATES")
    print("==============================")
    print()

    print("Origin Region")
    print("-------------")
    print(origin_region)
    print()

    print("Candidates :", len(candidates))
    print()

    for candidate in candidates:
        print(candidate)


if __name__ == "__main__":
    main()