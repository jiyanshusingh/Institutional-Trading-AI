from engines.data_engine import DataEngine
from services.market_analysis_engine import MarketAnalysisEngine

from policies.order_block.ict.ict_order_block_candidate_generator import (
    ICTOrderBlockCandidateGenerator
)

from policies.order_block.ict.ict_projection_policy import (
    ICTProjectionPolicy
)


def main():

    # Build market configuration
    data = DataEngine()

    df = data.get_data(
        "RELIANCE.NS",
        period="1y",
        interval="1d"
    )

    engine = MarketAnalysisEngine()

    configuration = engine.analyze(df)

    # Get Origin Region
    origin_region = configuration.origin_regions[0]

    # Generate Order Block Candidates
    generator = ICTOrderBlockCandidateGenerator()

    candidates = generator.generate(
        origin_region,
        configuration
    )

    # Select Candidate
    policy = ICTProjectionPolicy()

    selected_candidate = policy.select(
        candidates
    )

    print()
    print("============================")
    print("ICT PROJECTION POLICY")
    print("============================")
    print()

    print("Origin Region")
    print("-------------")
    print(origin_region)

    print()

    print("Candidates")
    print("----------")

    for candidate in candidates:
        print(candidate)

    print()

    print("Selected Candidate")
    print("------------------")
    print(selected_candidate)


if __name__ == "__main__":
    main()