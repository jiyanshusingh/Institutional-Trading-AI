from engines.data_engine import DataEngine
from services.market_analysis_engine import MarketAnalysisEngine

from policies.origin_region.ict.ict_origin_candidate_generator import (
    ICTOriginCandidateGenerator
)

from policies.origin_region.ict.ict_origin_selection_policy import (
    ICTOriginSelectionPolicy
)

from engines.origin_region_builder import OriginRegionBuilder


def main():

    # ----------------------------------
    # Load Data
    # ----------------------------------

    data = DataEngine()

    df = data.get_data(
        "RELIANCE.NS",
        period="1y",
        interval="1d"
    )

    # ----------------------------------
    # Build Market Configuration
    # ----------------------------------

    engine = MarketAnalysisEngine()

    configuration = engine.analyze(df)

    expansion = configuration.latest_expansion()

    if expansion is None:
        print("No Expansion Found")
        return

    # ----------------------------------
    # Generate Candidates
    # ----------------------------------

    generator = ICTOriginCandidateGenerator()

    candidates = generator.generate(
        expansion,
        configuration
    )

    # ----------------------------------
    # Select Candidate
    # ----------------------------------

    selector = ICTOriginSelectionPolicy()

    selected_candidate = selector.select(
        candidates
    )

    # ----------------------------------
    # Build Origin Region
    # ----------------------------------

    builder = OriginRegionBuilder()

    origin_region = builder.build(
        selected_candidate,
        expansion,
        configuration
    )

    # ----------------------------------
    # Output
    # ----------------------------------

    print()

    print("============================")
    print("ORIGIN REGION BUILDER")
    print("============================")

    print()

    print("Expansion")
    print("---------")
    print(expansion)

    print()

    print("Selected Candidate")
    print("------------------")
    print(selected_candidate)

    print()

    print("Origin Region")
    print("-------------")
    print(origin_region)


if __name__ == "__main__":
    main()