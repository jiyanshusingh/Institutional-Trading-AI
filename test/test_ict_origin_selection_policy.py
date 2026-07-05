from engines.data_engine import DataEngine
from services.market_analysis_engine import MarketAnalysisEngine

from policies.origin_region.ict.ict_origin_candidate_generator import (
    ICTOriginCandidateGenerator
)

from policies.origin_region.ict.ict_origin_selection_policy import (
    ICTOriginSelectionPolicy
)


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

    selected = selector.select(
        candidates
    )

    # ----------------------------------
    # Output
    # ----------------------------------

    print()

    print("============================")
    print("ICT ORIGIN SELECTION POLICY")
    print("============================")

    print()

    print("Expansion")
    print(expansion)

    print()

    print("Candidates")
    print("----------")

    for candidate in candidates:
        print(candidate)

    print()

    print("Selected Candidate")
    print("------------------")
    print(selected)


if __name__ == "__main__":
    main()